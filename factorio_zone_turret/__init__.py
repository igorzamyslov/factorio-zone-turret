import logging


LOGGING_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)

