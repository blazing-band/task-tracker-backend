import sys
from logging.config import dictConfig


def set_up_logger() -> None:
    logger_conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console_stdout": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "verbose",
            },
            "console_stderr": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "stream": sys.stderr,
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console_stdout", "console_stderr"],
                "level": "INFO",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["console_stdout", "console_stderr"],
                "level": "INFO",
                "propagate": False,
            },
            "root": {
                "handlers": ["console_stdout", "console_stderr"],
                "level": "INFO",
            },
        },
    }

    dictConfig(logger_conf)
