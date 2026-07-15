# Binance Trading Bot

A simple, structured command-line trading bot for Binance.
This project focuses on clean architecture by separating API communication, business logic, parameter validation, and CLI components.

## Project Structure

- `bot/client.py`: Handles direct communication with the Binance API.
- `bot/orders.py`: Contains business logic for orchestrating order execution.
- `bot/validators.py`: Handles parameter validation for commands.
- `bot/logging_config.py`: Sets up application logging to write to `logs/trading_bot.log`.
- `bot/cli.py`: The command-line interface entry point.

## Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables by creating a `.env` file for your API credentials (to be used later).

## Running the Bot

Run the CLI module passing in the required arguments:

```bash
# Example for a Market Order
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Example for a Limit Order
python -m bot.cli --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000
```
