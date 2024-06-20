import logging
import sys
import socket
from logging.handlers import TimedRotatingFileHandler


class Logger:
    FORMATTER_STRING = f"%(asctime)s — {socket.gethostbyname(socket.gethostname())} — %(name)s" \
                       f" — %(levelname)s — %(message)s"
    FORMATTER = logging.Formatter(FORMATTER_STRING)
    LOG_FILE = "logs.log"

    def __init__(self, name: str, console_out: bool = False):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if console_out:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(Logger.FORMATTER)
            logger.addHandler(stdout_handler)

        file_handler = TimedRotatingFileHandler(Logger.LOG_FILE, when='midnight')
        file_handler.setFormatter(Logger.FORMATTER)        
        logger.addHandler(file_handler)

        self.logger = logger

    def add_debug(self, text: str):
        self.logger.debug(text)

    def add_info(self, text: str):
        self.logger.info(text)

    def add_warning(self, text: str):
        self.logger.warning(text)

    def add_error(self, text: str):
        self.logger.error(text)
