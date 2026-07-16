"""
Lightweight Flask Server providing a Web UI for the Binance Trading Bot.
Acts as a thin presentation layer over the existing bot backend.
"""

from flask import Flask, send_from_directory, request, jsonify
from bot.client import BinanceClient
from bot.orders import OrderService
from bot.validators import OrderValidator
from bot.logging_config import setup_logger
import os

app = Flask(__name__, static_folder='frontend')
logger = setup_logger()

@app.route('/')
def index():
    """Serve the main frontend HTML file."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static CSS and JS files."""
    return send_from_directory(app.static_folder, path)

@app.route('/api/order', methods=['POST'])
def place_order():
    """
    API endpoint to place an order.
    Receives JSON containing symbol, side, type, quantity, and optionally price.
    Delegates to the existing OrderService.
    """
    data = request.json
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON payload"}), 400

    symbol = data.get("symbol", "").upper()
    side = data.get("side", "").upper()
    order_type = data.get("type", "").upper()
    
    # Securely parse numeric values
    try:
        quantity = float(data.get("quantity", 0))
    except (ValueError, TypeError):
        quantity = 0

    try:
        price = float(data.get("price", 0)) if data.get("price") else None
    except (ValueError, TypeError):
        price = None

    # 1. Input Validation using the exact existing logic
    validator = OrderValidator()
    try:
        validator.validate_symbol(symbol)
        validator.validate_side(side)
        validator.validate_order_type(order_type)
        validator.validate_quantity(quantity)
        if order_type == "LIMIT":
            validator.validate_price(price)
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

    # 2. Instantiate backend client
    try:
        client = BinanceClient()
        order_service = OrderService(client)
    except Exception as e:
        logger.error(f"Failed to initialize backend: {e}")
        return jsonify({"success": False, "error": "Internal server error connecting to backend."}), 500

    # 3. Delegate execution
    if order_type == "MARKET":
        response = order_service.execute_market_order(symbol, side, quantity)
    else:
        response = order_service.execute_limit_order(symbol, side, quantity, price)

    # OrderService already returns {"success": bool, "data": dict, "error": str}
    status_code = 200 if response.get("success") else 400
    return jsonify(response), status_code


if __name__ == "__main__":
    logger.info("Starting Flask Web UI...")
    app.run(debug=True, port=5000)
