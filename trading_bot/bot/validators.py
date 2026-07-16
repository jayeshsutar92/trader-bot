class OrderValidator:

    def validate_symbol(self, symbol: str) -> bool:
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol must be a non-empty string.")
            
        if not symbol.isupper():
            raise ValueError(f"Symbol '{symbol}' must be fully uppercase (e.g., 'BTCUSDT').")
            
        return True

    def validate_side(self, side: str) -> bool:
        if not side or not isinstance(side, str):
            raise ValueError("Side must be a non-empty string.")
            
        if side not in ["BUY", "SELL"]:
            raise ValueError(f"Invalid side '{side}'. Must be 'BUY' or 'SELL'.")
            
        return True

    def validate_order_type(self, order_type: str) -> bool:
        if not order_type or not isinstance(order_type, str):
            raise ValueError("Order type must be a non-empty string.")
            
        if order_type not in ["MARKET", "LIMIT", "STOP_LIMIT"]:
            raise ValueError(
                f"Invalid order type '{order_type}'. Must be 'MARKET', 'LIMIT', or 'STOP_LIMIT'."
            )
            
        return True

    def validate_quantity(self, quantity: float) -> bool:
        if quantity is None or not isinstance(quantity, (int, float)):
            raise ValueError("Quantity must be a numeric value.")
            
        if quantity <= 0:
            raise ValueError(f"Invalid quantity {quantity}. Must be a positive number greater than zero.")
            
        return True

    def validate_price(self, price: float) -> bool:
        if price is None:
            raise ValueError("Price is required for LIMIT and STOP_LIMIT orders.")
            
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a numeric value.")
            
        if price <= 0:
            raise ValueError(f"Invalid price {price}. Must be a positive number greater than zero.")
            
        return True

    def validate_stop_price(self, stop_price: float) -> bool:
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_LIMIT orders.")
            
        if not isinstance(stop_price, (int, float)):
            raise ValueError("Stop price must be a numeric value.")
            
        if stop_price <= 0:
            raise ValueError(f"Invalid stop price {stop_price}. Must be a positive number greater than zero.")
            
        return True