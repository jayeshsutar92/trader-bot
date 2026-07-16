# Binance Futures Trading Bot

## Project Overview
This project is a clean, structured command-line interface (CLI) application for executing trading orders on the Binance Futures Testnet. Built with pure Python, it emphasizes separation of concerns, clean architecture, and readability. It includes dedicated modules for API communication, business logic orchestration, robust input validation, and centralized logging.

## Prerequisites
- Python 3.8+
- An active internet connection
- A Binance Futures Testnet account (for generating API keys)

## Project Structure
```text
trading_bot/
│
├── bot/
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface entry point
│   ├── client.py           # Direct communication with Binance API
│   ├── logging_config.py   # Centralized logging setup
│   ├── orders.py           # Business logic for order execution
│   └── validators.py       # Input validation rules
│
├── logs/                   # Directory containing application logs (auto-generated)
├── .env                    # Secret environment variables (ignored in version control)
├── .env.example            # Template for environment variables
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   cd trading_bot
   ```

2. Create a virtual environment and activate it:
   ```bash
   # On macOS / Linux
   python -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup
The application reads sensitive credentials from a `.env` file to ensure security. 

1. Create a copy of the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and replace the placeholder text with your actual Binance Futures Testnet API Key and Secret.

## CLI Usage

The bot is executed from the command line by running the `bot.cli` module. It accepts the following arguments:

- `--symbol`: The trading pair symbol (e.g., BTCUSDT). **Required**.
- `--side`: The order side (BUY or SELL). **Required**.
- `--type`: The order type (MARKET or LIMIT). **Required**.
- `--quantity`: The amount of the asset to trade. Must be greater than 0. **Required**.
- `--price`: The limit price. **Required** only if the type is LIMIT.

### Example MARKET Command
Execute an immediate market order:
```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Example LIMIT Command
Place a limit order at a specific price:
```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000
```

## Assumptions
- **Environment:** The script assumes it is being run against the Binance Futures Testnet, not the live production network.
- **Order Details:** All limit orders are automatically submitted as Good-Til-Cancelled (`GTC`) to align with standard Futures behavior.
- **Python Setup:** The end user is familiar with creating virtual environments and passing command line arguments.
