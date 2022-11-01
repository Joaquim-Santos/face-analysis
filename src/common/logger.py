import logging
import sys
import os
import glob
import time
import pytz

from typing import Literal
from pathlib import Path
from datetime import date, datetime
from typing import Union


class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""

    @staticmethod
    def converter(timestamp: float) -> datetime:
        target_date = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        return target_date.astimezone(pytz.timezone("America/Sao_Paulo"))

    def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> str:
        target_date = self.converter(record.created)

        if datefmt:
            str_date = target_date.strftime(datefmt)
        else:
            try:
                str_date = target_date.isoformat(timespec="milliseconds")
            except TypeError:
                str_date = target_date.isoformat()

        return str_date


class Logger:
    def __init__(
        self, name: str, level: Literal[20] = logging.INFO, has_log_file: bool = True
    ) -> None:

        self.__log = None
        self.__log_file_name = ""
        self.__expiration_days = 30
        self.__has_log_file = has_log_file

        self.__log = self.get_logger(name, level)

    @property
    def log(self) -> logging.Logger:
        return self.__log

    @property
    def log_file_name(self) -> str:
        return self.__log_file_name

    def __remove_expired_files(self, log_file_path: Union[str, Path]) -> None:
        expiration_seconds = time.time() - (self.__expiration_days * 24 * 60 * 60)

        log_file_path = os.path.join(log_file_path, "*")
        files = glob.glob(log_file_path)

        for log_file in files:
            last_change_time = os.stat(log_file).st_ctime

            if expiration_seconds >= last_change_time:
                os.remove(log_file)  # pragma: no cover

    def __set_log_file_name(self, name: str) -> None:
        log_file_path = os.path.join(
            os.path.realpath(__file__), *["..", "..", "..", "logs"]
        )
        log_file_path = os.path.normpath(log_file_path)
        log_file_path = Path(log_file_path)

        log_file_path.mkdir(parents=True, exist_ok=True)
        self.__remove_expired_files(log_file_path)

        log_file_name = os.path.join(log_file_path, f"{name}-{date.today()}.log")
        self.__log_file_name = log_file_name

    def get_logger(
        self, name: str, level: Literal[20] = logging.INFO
    ) -> logging.Logger:

        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = Formatter(log_format, "%Y-%m-%d %H:%M:%S")

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        logging.basicConfig(format=log_format, handlers=[stream_handler])

        logger = logging.getLogger(name)
        logger.setLevel(level)

        if self.__has_log_file:  # Lambda na AWS não aceita geração de arquivos.
            self.__set_log_file_name(name)

            file_handler = logging.FileHandler(
                filename=self.__log_file_name, encoding="UTF-8"
            )

            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger
