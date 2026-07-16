import os

from binance.client import Client
from binance.exceptions import (
    BinanceAPIException,
    BinanceOrderException,
    BinanceRequestException
)
from dotenv import load_dotenv

from bot.logging_config import setup_logger


load_dotenv()
logger = setup_logger()


class BinanceClient:

    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = True):
        if not api_key or api_key == "placeholder_key":
            api_key = os.getenv("BINANCE_API_KEY")
            
        if not api_secret or api_secret == "placeholder_secret":
            api_secret = os.getenv("BINANCE_API_SECRET")
            
        if not api_key or not api_secret:
            logger.warning("Binance API credentials not found. Requests may fail.")
            
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
        logger.info(f"Binance client initialized (Futures Testnet: {self.testnet})")

    def _handle_exception(self, e: Exception, order_type: str):
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

    def place_stop_limit_order(
        self, symbol: str, side: str, quantity: float, price: float, stop_price: float
    ) -> dict:
        logger.info(
            f"Sending STOP_LIMIT order request: {side} {quantity} {symbol} "
            f"at limit {price}, stop {stop_price}"
        )
        try:
            response = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                stopPrice=stop_price
            )
            logger.info(f"STOP_LIMIT order successful. Response: {response}")
            return response
        except Exception as e:
            self._handle_exception(e, "STOP_LIMIT")