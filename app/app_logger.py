import logging.handlers
import os
import sys

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging_level = logging.INFO

if "DEBUG" in os.environ:
    logging_level = logging.DEBUG
    print("enabled logging debug")

logging.basicConfig(level=logging_level, format=LOG_FORMAT, force=True)

logger = logging.getLogger()


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception