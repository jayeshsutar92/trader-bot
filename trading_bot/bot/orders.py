"""
Service layer for executing trading orders.
Separates business logic from the direct API client calls.
"""

from bot.client import BinanceClient

class OrderService:
    """
    Handles the business logic for creating and executing orders.
    """

    def __init__(self, client: BinanceClient):
        """
        Initialize the order service.

        Args:
            client (BinanceClient): The initialized Binance API client.
        """
        self.client = client

    def execute_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        Execute a market order by communicating with the client.

        Args:
            symbol (str): The trading pair symbol.
            side (str): The order side.
            quantity (float): The amount to trade.

        Returns:
            dict: The result of the order execution.
        """
        return self.client.place_market_order(symbol, side, quantity)

    def execute_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        """
        Execute a limit order by communicating with the client.

        Args:
            symbol (str): The trading pair symbol.
            side (str): The order side.
            quantity (float): The amount to trade.
            price (float): The limit price.

        Returns:
            dict: The result of the order execution.
        """
        return self.client.place_limit_order(symbol, side, quantity, price)
