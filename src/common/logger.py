import logging
import sys
import os
import glob

from typing import Literal
from pathlib import Path
from datetime import date
from typing import Union


class Logger:
    def __init__(self, name: str, level: Literal[20] = logging.INFO) -> None:
        self.__log = None
        self.__log_file_name = ''
        self.__expiration_days = 30

        self.__log = self.get_logger(name, level)

    @property
    def log(self) -> logging.Logger:
        return self.__log

    @property
    def log_file_name(self) -> str:
        return self.__log_file_name

    def __remove_expired_files(self, log_file_path: Union[str, Path]) -> None:
        files_count = os.listdir(log_file_path)

        if len(files_count) > self.__expiration_days:
            log_file_path = os.path.join(log_file_path, '*')
            files = glob.glob(log_file_path)

            for log_file in files:
                os.remove(log_file)

    def __set_log_file_name(self, name: str) -> None:
        log_file_path = os.path.join(os.path.realpath(__file__), *['..', '..', '..', 'logs'])
        log_file_path = os.path.normpath(log_file_path)
        log_file_path = Path(log_file_path)

        log_file_path.mkdir(parents=True, exist_ok=True)
        self.__remove_expired_files(log_file_path)

        log_file_name = os.path.join(log_file_path, f'{name}-{date.today()}.log')
        self.__log_file_name = log_file_name

    def get_logger(self, name: str, level: Literal[20] = logging.INFO) -> logging.Logger:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(format=log_format, handlers=[logging.StreamHandler(sys.stdout)])

        logger = logging.getLogger(name)
        logger.setLevel(level)

        formatter = logging.Formatter(log_format)
        self.__set_log_file_name(name)

        file_handler = logging.FileHandler(filename=self.__log_file_name, encoding="UTF-8")

        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
