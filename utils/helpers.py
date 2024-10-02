import logging
import os


def setup_logging(log_filename: str):
    """
    Set up logging configuration.

    Args:
        log_filename (str): The name of the log file where logs will be stored.
    """
    # Remove all handlers associated with the root logger object
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create the "logs" directory if it doesn't exist
    log_directory = os.path.dirname(log_filename)
    if log_directory and not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Set up logging
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    )
