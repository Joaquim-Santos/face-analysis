import logging
import sys
import os

from typing import Literal
from shutil import rmtree


class Logger:
    def __init__(self, name: str, level: Literal[20] = logging.INFO) -> None:
        self.__log = self.get_logger(name, level)
        self.__log_file_name = ''

    @property
    def log(self) -> logging.Logger:
        return self.__log

    @property
    def log_file_name(self) -> str:
        return self.__log_file_name

    def __set_log_file_name(self, name: str) -> None:
        log_file_path = os.path.join(os.path.realpath(__file__), *['..', '..', 'logs'])
        log_file_path = os.path.normpath(log_file_path)

        rmtree(log_file_path)
        os.mkdir(log_file_path)

        log_file_name = os.path.join(log_file_path, f'{name}.log')
        self.__log_file_name = log_file_name

    def get_logger(self, name: str, level: Literal[20] = logging.INFO) -> logging.Logger:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(format=log_format, handlers=[logging.StreamHandler(sys.stdout)])

        logger = logging.getLogger(name)
        logger.setLevel(level)

        formatter = logging.Formatter(log_format)
        self.__set_log_file_name(name)

        file_handler = logging.FileHandler(filename=self.__log_file_name, encoding="UTF-8")

        file_handler.suffix = "%Y%m%d"
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
