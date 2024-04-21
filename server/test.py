import os
import logging.config

LOG_FILE = os.path.join('./', 'request.log')
LOGGER_LEVEL = "DEBUG"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": LOG_FILE
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        }
    },
    "loggers": {
        "backendapp": {
            "handlers": ["file", "console"],
            "level": LOGGER_LEVEL,
            "propagate": False
        }
    },
}

logging.config.dictConfig(LOGGING)

console_logger = logging.getLogger("backendapp")
file_logger = logging.getLogger("backendapp")

# Test log messages
console_logger.debug('This is a debug message for console')
console_logger.info('This is an info message for console')
console_logger.warning('This is a warning message for console')

file_logger.error('This is an error message for file')
file_logger.critical('This is a critical message for file')
