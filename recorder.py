import logging
import logging.handlers

logger = None


def setup_output(directory=".") -> None:
    global logger

    handler = logging.handlers.TimedRotatingFileHandler(directory+"/log.txt", when="midnight")
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)


def save_data_block(data_buffer: bytearray) -> None:
    logger.error(data_buffer.hex(" "))
