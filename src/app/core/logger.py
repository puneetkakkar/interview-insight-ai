import logging
import sys
from typing import Any

from .config import settings

# Configure logging
def setup_logger() -> logging.Logger:
    """Setup and configure the application logger."""
    logger = logging.getLogger("fastapi-minimal")
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_logger()
