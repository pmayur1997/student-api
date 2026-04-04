import os 
from loguru import logger

os.makedirs("logs",exist_ok=True)
logger.remove()

# Console logger
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    level="INFO",
    colorize=True
)

# ── File logger (all logs) ───────────────────────
logger.add(
    sink="logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="1 day",       # new file every day
    retention="7 days",     # keep logs for 7 days
    compression="zip"       # compress old logs
)

# ── Error file logger (errors only) ─────────────
logger.add(
    sink="logs/error.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="ERROR",
    rotation="1 week",
    retention="1 month",
    compression="zip"
)