import os
from flask import Flask, send_from_directory, request, jsonify

from bot.client import BinanceClient
from bot.orders import OrderService
from bot.validators import OrderValidator
from bot.logging_config import setup_logger


app = Flask(__name__, static_folder='frontend')
logger = setup_logger()


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)


@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON payload"}), 400

    symbol = data.get("symbol", "").upper()
    side = data.get("side", "").upper()
    order_type = data.get("type", "").upper()

    try:
        quantity = float(data.get("quantity", 0))
    except (ValueError, TypeError):
        quantity = 0

    try:
        price = float(data.get("price", 0)) if data.get("price") else None
    except (ValueError, TypeError):
        price = None

    try:
        stop_price = float(data.get("stopPrice", 0)) if data.get("stopPrice") else None
    except (ValueError, TypeError):
        stop_price = None

    validator = OrderValidator()
    
    try:
        validator.validate_symbol(symbol)
        validator.validate_side(side)
        validator.validate_order_type(order_type)
        validator.validate_quantity(quantity)
        
        if order_type in ["LIMIT", "STOP_LIMIT"]:
            validator.validate_price(price)
            
        if order_type == "STOP_LIMIT":
            validator.validate_stop_price(stop_price)
            
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400

    try:
        client = BinanceClient()
        order_service = OrderService(client)
    except Exception as e:
        logger.error(f"Failed to initialize backend: {e}")
        return jsonify(
            {"success": False, "error": "Internal server error connecting to backend."}
        ), 500

    if order_type == "MARKET":
        response = order_service.execute_market_order(symbol, side, quantity)
    elif order_type == "LIMIT":
        response = order_service.execute_limit_order(symbol, side, quantity, price)
    elif order_type == "STOP_LIMIT":
        response = order_service.execute_stop_limit_order(
            symbol, side, quantity, price, stop_price
        )
    else:
        response = {"success": False, "error": "Unsupported order type."}

    status_code = 200 if response.get("success") else 400
    
    return jsonify(response), status_code


if __name__ == "__main__":
    logger.info("Starting Flask Web UI...")
    app.run(debug=True, port=5000)