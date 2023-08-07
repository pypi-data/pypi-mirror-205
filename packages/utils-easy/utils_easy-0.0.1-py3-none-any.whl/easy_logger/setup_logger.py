import logging
import logging.config
import os
from .logging_config import LOGGING_CONFIG

def setup_logger(module_name):
    # Set the log file path
    log_dir = f"./logs"
    filepath = os.path.join(log_dir,f"{module_name}_log.txt")
    LOGGING_CONFIG["handlers"]["file"]["filename"] = filepath

    os.makedirs(log_dir, exist_ok=True)

    # apply configuration
    logging.config.dictConfig(LOGGING_CONFIG)

    # create logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
    
    if not logger.handlers:
        # # get handler from config
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOGGING_CONFIG["handlers"]["console"]["level"])
        console_handler.setFormatter(logging.Formatter(LOGGING_CONFIG["formatters"]["default"]["format"]))


        file_handler = logging.FileHandler(filepath)
        file_handler.setLevel(LOGGING_CONFIG["handlers"]["file"]["level"])
        file_handler.setFormatter(logging.Formatter(LOGGING_CONFIG["formatters"]["default"]["format"]))
        

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.propagate = False

    return logger