import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """Setup logging for both console and file."""
    # Create a file handler that logs messages to a file, rotating every 1 MB
    file_handler = RotatingFileHandler(f"{app.name}.log", maxBytes=1 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.INFO)  # Set the log level for file handler
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # Log format

    # Create a stream handler for console logging
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Set the log level for console handler
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # Log format

    # Add handlers to the Flask app's logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)

    # Set the global log level (this will apply to all handlers)
    app.logger.setLevel(logging.INFO)
