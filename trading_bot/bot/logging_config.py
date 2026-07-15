"""
Configuration for the application's logging system.
"""

import logging
from pathlib import Path

def setup_logger() -> logging.Logger:
    """
    Configure and return the application logger.

    Ensures the logs directory exists so the file handler can write safely.

    Returns:
        logging.Logger: The configured logger instance.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "trading_bot.log"
    
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)
    
    # Avoid adding multiple handlers if the logger is already configured
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
