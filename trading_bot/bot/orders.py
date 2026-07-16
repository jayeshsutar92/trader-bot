"""
Service layer for executing trading orders.
Separates business logic from the direct API client calls.
"""

from bot.client import BinanceClient
from bot.validators import OrderValidator
from bot.logging_config import setup_logger

# Initialize the module-level logger
logger = setup_logger()


class OrderService:
    """
    Handles the business logic for creating and executing orders.
    Provides validation and graceful error handling before passing
    requests to the Binance API client.
    """

    def __init__(self, client: BinanceClient):
        """
        Initialize the order service.

        Args:
            client (BinanceClient): The initialized Binance API client.
        """
        self.client = client
        self.validator = OrderValidator()

    def _create_response(self, success: bool, data: dict = None, error_message: str = None) -> dict:
        """
        Helper method to create a clean, consistent response dictionary.
        
        Args:
            success (bool): Whether the operation was successful.
            data (dict, optional): The payload from the operation.
            error_message (str, optional): A descriptive error message if it failed.
            
        Returns:
            dict: The standardized response object.
        """
        return {
            "success": success,
            "data": data,
            "error": error_message
        }

    def execute_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        Validate inputs and execute a market order.

        Args:
            symbol (str): The trading pair symbol.
            side (str): The order side.
            quantity (float): The amount to trade.

        Returns:
            dict: A standard response dictionary containing success status, data, or error message.
        """
        logger.info(f"OrderService: Validating MARKET order for {quantity} {symbol} ({side})")
        
        # 1. Input Validation
        if not self.validator.validate_symbol(symbol):
            logger.warning(f"OrderService: Invalid symbol '{symbol}'")
            return self._create_response(False, error_message="Invalid symbol provided.")
            
        if not self.validator.validate_side(side):
            logger.warning(f"OrderService: Invalid side '{side}'")
            return self._create_response(False, error_message="Invalid side provided. Must be BUY or SELL.")
            
        if not self.validator.validate_quantity(quantity):
            logger.warning(f"OrderService: Invalid quantity '{quantity}'")
            return self._create_response(False, error_message="Invalid quantity. Must be greater than zero.")
            
        # 2. Execution and Exception Handling
        try:
            logger.info("OrderService: Validation passed, delegating to Binance client.")
            response = self.client.place_market_order(symbol, side, quantity)
            return self._create_response(True, data=response)
        except Exception as e:
            logger.error(f"OrderService: Failed to execute MARKET order. Error: {str(e)}")
            return self._create_response(False, error_message=f"Order failed: {str(e)}")

    def execute_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        """
        Validate inputs and execute a limit order.

        Args:
            symbol (str): The trading pair symbol.
            side (str): The order side.
            quantity (float): The amount to trade.
            price (float): The limit price.

        Returns:
            dict: A standard response dictionary containing success status, data, or error message.
        """
        logger.info(f"OrderService: Validating LIMIT order for {quantity} {symbol} ({side}) at {price}")
        
        # 1. Input Validation
        if not self.validator.validate_symbol(symbol):
            logger.warning(f"OrderService: Invalid symbol '{symbol}'")
            return self._create_response(False, error_message="Invalid symbol provided.")
            
        if not self.validator.validate_side(side):
            logger.warning(f"OrderService: Invalid side '{side}'")
            return self._create_response(False, error_message="Invalid side provided. Must be BUY or SELL.")
            
        if not self.validator.validate_quantity(quantity):
            logger.warning(f"OrderService: Invalid quantity '{quantity}'")
            return self._create_response(False, error_message="Invalid quantity. Must be greater than zero.")
            
        if not self.validator.validate_price(price):
            logger.warning(f"OrderService: Invalid price '{price}'")
            return self._create_response(False, error_message="Invalid price. Must be greater than zero.")

        # 2. Execution and Exception Handling
        try:
            logger.info("OrderService: Validation passed, delegating to Binance client.")
            response = self.client.place_limit_order(symbol, side, quantity, price)
            return self._create_response(True, data=response)
        except Exception as e:
            logger.error(f"OrderService: Failed to execute LIMIT order. Error: {str(e)}")
            return self._create_response(False, error_message=f"Order failed: {str(e)}")
