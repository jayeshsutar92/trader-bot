"""
Command Line Interface (CLI) entrypoint for the trading bot application.
"""

import argparse
import sys
import os

# Add the parent directory to sys.path so 'bot' package is recognized
# when running cli.py directly as a script.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.client import BinanceClient
from bot.orders import OrderService
from bot.logging_config import setup_logger
from bot.validators import OrderValidator

def main():
    """
    Main entry point for parsing arguments and initializing bot components.
    """
    parser = argparse.ArgumentParser(description="Binance Trading Bot CLI")
    
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="Order side (BUY or SELL)")
    parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT"], help="Order type (MARKET or LIMIT)")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, required=False, help="Price for limit order")
    
    args = parser.parse_args()
    
    # Instantiate the logger
    logger = setup_logger()
    
    # Instantiate the validator
    validator = OrderValidator()
    
    # Perform validation on the inputs
    if not validator.validate_symbol(args.symbol):
        logger.error(f"Invalid symbol: {args.symbol}")
        print("Error: Invalid symbol provided.")
        return
        
    if not validator.validate_side(args.side):
        logger.error(f"Invalid side: {args.side}")
        print("Error: Invalid side provided.")
        return
        
    if not validator.validate_order_type(args.type):
        logger.error(f"Invalid order type: {args.type}")
        print("Error: Invalid order type provided.")
        return
        
    if not validator.validate_quantity(args.quantity):
        logger.error(f"Invalid quantity: {args.quantity}")
        print("Error: Invalid quantity provided.")
        return
        
    if args.type == "LIMIT":
        if args.price is None or not validator.validate_price(args.price):
            logger.error("Limit order requires a valid price.")
            print("Error: Limit order requires a valid price.")
            return

    # Instantiate API client and order service (using placeholders for credentials)
    api_key = "placeholder_key"
    api_secret = "placeholder_secret"
    
    client = BinanceClient(api_key=api_key, api_secret=api_secret, testnet=True)
    order_service = OrderService(client)
    
    print("Project scaffold initialized.")

if __name__ == "__main__":
    main()
