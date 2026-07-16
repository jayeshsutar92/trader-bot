from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.validators import OrderValidator

logger = setup_logger()

class OrderService:

    def __init__(self, client: BinanceClient):
        self.client = client
        self.validator = OrderValidator()

    def _create_response(self, success: bool, data: dict = None, error_message: str = None) -> dict:
        return {
            "success": success,
            "data": data,
            "error": error_message
        }

    def execute_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        logger.info(f"OrderService: Validating MARKET order for {quantity} {symbol} ({side})")
        
        if not self.validator.validate_symbol(symbol):
            logger.warning(f"OrderService: Invalid symbol '{symbol}'")
            return self._create_response(False, error_message="Invalid symbol provided.")
            
        if not self.validator.validate_side(side):
            logger.warning(f"OrderService: Invalid side '{side}'")
            return self._create_response(
                False, error_message="Invalid side provided. Must be BUY or SELL."
            )
            
        if not self.validator.validate_quantity(quantity):
            logger.warning(f"OrderService: Invalid quantity '{quantity}'")
            return self._create_response(
                False, error_message="Invalid quantity. Must be greater than zero."
            )
            
        try:
            logger.info("OrderService: Validation passed, delegating to Binance client.")
            response = self.client.place_market_order(symbol, side, quantity)
            return self._create_response(True, data=response)
        except Exception as e:
            logger.error(f"OrderService: Failed to execute MARKET order. Error: {str(e)}")
            return self._create_response(False, error_message=f"Order failed: {str(e)}")

    def execute_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        logger.info(f"OrderService: Validating LIMIT order for {quantity} {symbol} ({side}) at {price}")
        
        if not self.validator.validate_symbol(symbol):
            logger.warning(f"OrderService: Invalid symbol '{symbol}'")
            return self._create_response(False, error_message="Invalid symbol provided.")
            
        if not self.validator.validate_side(side):
            logger.warning(f"OrderService: Invalid side '{side}'")
            return self._create_response(
                False, error_message="Invalid side provided. Must be BUY or SELL."
            )
            
        if not self.validator.validate_quantity(quantity):
            logger.warning(f"OrderService: Invalid quantity '{quantity}'")
            return self._create_response(
                False, error_message="Invalid quantity. Must be greater than zero."
            )
            
        if not self.validator.validate_price(price):
            logger.warning(f"OrderService: Invalid price '{price}'")
            return self._create_response(
                False, error_message="Invalid price. Must be greater than zero."
            )
            
        try:
            logger.info("OrderService: Validation passed, delegating to Binance client.")
            response = self.client.place_limit_order(symbol, side, quantity, price)
            return self._create_response(True, data=response)
        except Exception as e:
            logger.error(f"OrderService: Failed to execute LIMIT order. Error: {str(e)}")
            return self._create_response(False, error_message=f"Order failed: {str(e)}")

    def execute_stop_limit_order(
        self, symbol: str, side: str, quantity: float, price: float, stop_price: float
    ) -> dict:
        logger.info(
            f"OrderService: Validating STOP_LIMIT order for {quantity} {symbol} "
            f"({side}) at limit {price}, stop {stop_price}"
        )
        
        if not self.validator.validate_symbol(symbol):
            logger.warning(f"OrderService: Invalid symbol '{symbol}'")
            return self._create_response(False, error_message="Invalid symbol provided.")
            
        if not self.validator.validate_side(side):
            logger.warning(f"OrderService: Invalid side '{side}'")
            return self._create_response(
                False, error_message="Invalid side provided. Must be BUY or SELL."
            )
            
        if not self.validator.validate_quantity(quantity):
            logger.warning(f"OrderService: Invalid quantity '{quantity}'")
            return self._create_response(
                False, error_message="Invalid quantity. Must be greater than zero."
            )
            
        if not self.validator.validate_price(price):
            logger.warning(f"OrderService: Invalid price '{price}'")
            return self._create_response(
                False, error_message="Invalid price. Must be greater than zero."
            )
            
        if not self.validator.validate_stop_price(stop_price):
            logger.warning(f"OrderService: Invalid stop price '{stop_price}'")
            return self._create_response(
                False, error_message="Invalid stop price. Must be greater than zero."
            )
            
        try:
            logger.info("OrderService: Validation passed, delegating to Binance client.")
            response = self.client.place_stop_limit_order(symbol, side, quantity, price, stop_price)
            return self._create_response(True, data=response)
        except Exception as e:
            logger.error(f"OrderService: Failed to execute STOP_LIMIT order. Error: {str(e)}")
            return self._create_response(False, error_message=f"Order failed: {str(e)}")