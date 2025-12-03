import logging

def setup_logging(debug=False):
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging_level = logging.DEBUG if debug else logging.INFO
    logging_datefmt = "%H:%M:%S"

    # logging_formatter = logging.Formatter(fmt=logging_format, datefmt=logging_datefmt)

    logging.basicConfig(format=logging_format, level=logging_level, datefmt=logging_datefmt)

    logger = logging.getLogger('__name__')
