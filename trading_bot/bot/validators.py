"""
Input validation components to ensure correct parameters before order execution.
"""

class OrderValidator:
    """
    Validates order parameters such as symbol, side, type, quantity, and price.
    """

    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate the trading pair symbol.

        Args:
            symbol (str): The trading pair symbol to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not isinstance(symbol, str) or not symbol:
            return False
        return True

    def validate_side(self, side: str) -> bool:
        """
        Validate the order side.

        Args:
            side (str): The order side ('BUY' or 'SELL').

        Returns:
            bool: True if valid, False otherwise.
        """
        valid_sides = ["BUY", "SELL"]
        return side.upper() in valid_sides

    def validate_order_type(self, order_type: str) -> bool:
        """
        Validate the order type.

        Args:
            order_type (str): The order type ('MARKET' or 'LIMIT').

        Returns:
            bool: True if valid, False otherwise.
        """
        valid_types = ["MARKET", "LIMIT"]
        return order_type.upper() in valid_types

    def validate_quantity(self, quantity: float) -> bool:
        """
        Validate the trade quantity.

        Args:
            quantity (float): The amount to trade.

        Returns:
            bool: True if valid (greater than zero), False otherwise.
        """
        return isinstance(quantity, (float, int)) and quantity > 0

    def validate_price(self, price: float) -> bool:
        """
        Validate the limit order price.

        Args:
            price (float): The price of the asset.

        Returns:
            bool: True if valid (greater than zero), False otherwise.
        """
        return isinstance(price, (float, int)) and price > 0
