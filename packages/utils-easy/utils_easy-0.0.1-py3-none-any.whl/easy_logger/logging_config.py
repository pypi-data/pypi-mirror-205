import os 
import logging

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s",

        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level":  "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "WARNING",
            "formatter": "default",
            "filename": "",
        },
    },
}