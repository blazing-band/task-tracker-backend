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
            "root": {
                # 'level': 'DEBUG' if settings.logger_settings.debug else 'INFO',
                "level": "INFO",
                "handlers": ["console_stdout", "console_stderr"],
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console_stdout", "console_stderr"],
                "level": "TRACE",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console_stdout", "console_stderr"],
                "level": "TRACE",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console_stdout", "console_stderr"],
                "level": "TRACE",
                "propagate": False,
            },
            "uvicorn.asgi": {
                "handlers": ["console_stdout", "console_stderr"],
                "level": "TRACE",
                "propagate": False,
            },
        },
    }

    dictConfig(logger_conf)
