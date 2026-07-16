"""
Command Line Interface (CLI) entrypoint for the trading bot application.
"""

import argparse
import sys
import os

# Ensure the 'bot' package can be found when executing this file directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.client import BinanceClient
from bot.orders import OrderService
from bot.logging_config import setup_logger
from bot.validators import OrderValidator

def main():
    """
    Main entry point for parsing arguments, validating inputs, and executing orders.
    """
    parser = argparse.ArgumentParser(description="Binance Trading Bot CLI")
    
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="Order side (BUY or SELL)")
    parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT"], help="Order type (MARKET or LIMIT)")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, required=False, help="Price for limit order")
    
    args = parser.parse_args()
    
    # Initialize components
    logger = setup_logger()
    validator = OrderValidator()

    # 1. Print Request Summary
    print("\n--- Order Request Summary ---")
    print(f"Symbol:   {args.symbol}")
    print(f"Side:     {args.side}")
    print(f"Type:     {args.type}")
    print(f"Quantity: {args.quantity}")
    if args.type == "LIMIT":
        print(f"Price:    {args.price}")
    print("-----------------------------\n")

    logger.info("Initializing trading bot CLI...")

    # 2. Input Validation
    try:
        validator.validate_symbol(args.symbol)
        validator.validate_side(args.side)
        validator.validate_order_type(args.type)
        validator.validate_quantity(args.quantity)
        if args.type == "LIMIT":
            validator.validate_price(args.price)
    except ValueError as e:
        logger.error(f"Validation Error: {e}")
        print(f"Validation Error: {e}")
        return

    # 3. Instantiate Client and Service
    try:
        client = BinanceClient()
        order_service = OrderService(client)
    except Exception as e:
        logger.error(f"Initialization Error: {e}")
        print(f"Initialization Error: {e}")
        return
    
    # 4. Execute Order
    print("Executing order...\n")
    try:
        if args.type == "MARKET":
            response = order_service.execute_market_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity
            )
        else:
            response = order_service.execute_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price
            )
        
        # 5. Print Response
        if response.get("success"):
            data = response.get("data", {})
            print("=== Order Successful ===")
            print(f"Order ID:    {data.get('orderId', 'N/A')}")
            print(f"Status:      {data.get('status', 'N/A')}")
            print(f"ExecutedQty: {data.get('executedQty', 'N/A')}")
            # Use avgPrice if available, fallback to price
            avg_price = data.get('avgPrice', data.get('price', 'N/A'))
            print(f"Avg Price:   {avg_price}")
            print("========================")
            logger.info(f"Order completed successfully. Order ID: {data.get('orderId')}")
        else:
            error_msg = response.get("error", "Unknown error occurred.")
            print("=== Order Failed ===")
            print(f"Reason: {error_msg}")
            print("====================")
            logger.error(f"Order failed: {error_msg}")

    except Exception as e:
        logger.error(f"Unexpected execution error: {e}")
        print("=== Order Failed ===")
        print(f"Unexpected Error: {e}")
        print("====================")


if __name__ == "__main__":
    main()
