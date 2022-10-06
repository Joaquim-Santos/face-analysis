import logging

from typing import Literal


class Logger:
    def __init__(self, name: str, level: Literal[20] = logging.INFO) -> None:
        self.log = self.get_logger(name, level)

    @staticmethod
    def get_logger(name: str, level: Literal[20] = logging.INFO) -> logging.Logger:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(format=log_format, handlers=[logging.StreamHandler()])

        logger = logging.getLogger(name)
        logger.setLevel(level)

        return logger
