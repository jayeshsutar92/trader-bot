"""
Command Line Interface for the Binance Trading Bot.
Provides an interactive Typer-based CLI for executing orders.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional

from bot.client import BinanceClient
from bot.orders import OrderService
from bot.logging_config import setup_logger

app = typer.Typer(help="Binance Futures Trading Bot CLI")
console = Console()
logger = setup_logger()

@app.callback(invoke_without_command=True)
def main(
    symbol: str = typer.Option(None, "--symbol", "-s", help="Trading pair symbol (e.g. BTCUSDT)"),
    side: str = typer.Option(None, "--side", help="Order side: BUY or SELL"),
    order_type: str = typer.Option(None, "--type", "-t", help="Order type: MARKET, LIMIT, or STOP_LIMIT"),
    quantity: float = typer.Option(None, "--quantity", "-q", help="Quantity to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Limit price (Required for LIMIT/STOP_LIMIT)"),
    stop_price: float = typer.Option(None, "--stop-price", help="Stop trigger price (Required for STOP_LIMIT)"),
):
    """
    Execute a trading order. If arguments are omitted, interactive prompts will appear.
    """
    # Interactive Prompts if missing
    if not symbol:
        symbol = typer.prompt("Enter symbol (e.g. BTCUSDT)").upper()
    if not side:
        side = typer.prompt("Enter side (BUY/SELL)").upper()
    if not order_type:
        order_type = typer.prompt("Enter order type (MARKET/LIMIT/STOP_LIMIT)").upper()
    if quantity is None:
        quantity = typer.prompt("Enter quantity", type=float)

    if order_type in ["LIMIT", "STOP_LIMIT"] and price is None:
        price = typer.prompt("Enter limit price", type=float)
        
    if order_type == "STOP_LIMIT" and stop_price is None:
        stop_price = typer.prompt("Enter stop trigger price", type=float)

    # Display Order Summary
    table = Table(title="Order Request Summary")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Symbol", symbol)
    table.add_row("Side", side)
    table.add_row("Type", order_type)
    table.add_row("Quantity", str(quantity))
    if order_type in ["LIMIT", "STOP_LIMIT"]:
        table.add_row("Price", str(price))
    if order_type == "STOP_LIMIT":
        table.add_row("Stop Price", str(stop_price))
        
    console.print(table)
    console.print("\n[yellow]Executing order...[/yellow]\n")

    try:
        client = BinanceClient()
        order_service = OrderService(client)
    except Exception as e:
        console.print(Panel(f"Failed to initialize client: {str(e)}", title="Initialization Error", border_style="red"))
        raise typer.Exit(1)

    if order_type == "MARKET":
        response = order_service.execute_market_order(symbol, side, quantity)
    elif order_type == "LIMIT":
        response = order_service.execute_limit_order(symbol, side, quantity, price)
    elif order_type == "STOP_LIMIT":
        response = order_service.execute_stop_limit_order(symbol, side, quantity, price, stop_price)
    else:
        console.print(Panel(f"Unsupported order type: {order_type}", title="Validation Error", border_style="red"))
        raise typer.Exit(1)

    # Display Results
    if response.get("success"):
        data = response.get("data", {})
        res_table = Table(title="Order Response Details")
        res_table.add_column("Key", style="green")
        res_table.add_column("Value", style="bold white")
        
        res_table.add_row("Order ID", str(data.get("orderId", "N/A")))
        res_table.add_row("Status", str(data.get("status", "N/A")))
        res_table.add_row("Executed Qty", str(data.get("executedQty", "N/A")))
        res_table.add_row("Avg Price", str(data.get("avgPrice", data.get("price", "N/A"))))
        
        console.print(Panel(res_table, title="Order Successful", border_style="green"))
    else:
        console.print(Panel(response.get("error", "Unknown error"), title="Order Failed", border_style="red"))
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
