"""
Handles direct communication with the Binance API.
"""

import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import (
    BinanceAPIException,
    BinanceOrderException,
    BinanceRequestException
)
from bot.logging_config import setup_logger

# Load environment variables from .env file
load_dotenv()

# Initialize the module-level logger
logger = setup_logger()


class BinanceClient:
    """
    Client for interacting with the Binance API, specifically Binance Futures.
    """

    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = True):
        """
        Initialize the Binance API client.

        Reads credentials from the .env file if placeholder values are passed
        from the CLI layer, ensuring security.

        Args:
            api_key (str): The user's Binance API key.
            api_secret (str): The user's Binance API secret.
            testnet (bool): Whether to use the Binance testnet (default is True).
        """
        # Override placeholders with environment variables
        if not api_key or api_key == "placeholder_key":
            api_key = os.getenv("BINANCE_API_KEY")
        
        if not api_secret or api_secret == "placeholder_secret":
            api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            logger.warning("Binance API credentials not found. Requests may fail.")

        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

        # Initialize the python-binance client
        self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
        logger.info(f"Binance client initialized (Futures Testnet: {self.testnet})")

    def _handle_exception(self, e: Exception, order_type: str):
        """
        Helper method to handle and log API, validation, and network exceptions.
        
        Args:
            e (Exception): The caught exception.
            order_type (str): The type of order being placed (MARKET or LIMIT).
        """
        if isinstance(e, BinanceAPIException):
            logger.error(f"API Exception ({order_type}): {e.status_code} - {e.message}")
        elif isinstance(e, BinanceOrderException):
            logger.error(f"Order Validation Exception ({order_type}): {e.status_code} - {e.message}")
        elif isinstance(e, BinanceRequestException):
            logger.error(f"Network/Request Exception ({order_type}): {e.message}")
        else:
            logger.error(f"Unexpected error ({order_type}): {str(e)}")
        
        raise e

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        Place a market order on Binance Futures.

        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            side (str): The order side ('BUY' or 'SELL').
            quantity (float): The amount to trade.

        Returns:
            dict: The parsed JSON response from the Binance API.
        """
        logger.info(f"Sending MARKET order request: {side} {quantity} {symbol}")
        try:
            response = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            logger.info(f"MARKET order successful. Response: {response}")
            return response
        except Exception as e:
            self._handle_exception(e, "MARKET")

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        """
        Place a limit order on Binance Futures.

        Args:
            symbol (str): The trading pair symbol.
            side (str): The order side ('BUY' or 'SELL').
            quantity (float): The amount to trade.
            price (float): The limit price.

        Returns:
            dict: The parsed JSON response from the Binance API.
        """
        logger.info(f"Sending LIMIT order request: {side} {quantity} {symbol} at {price}")
        try:
            response = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            logger.info(f"LIMIT order successful. Response: {response}")
            return response
        except Exception as e:
            self._handle_exception(e, "LIMIT")
