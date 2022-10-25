import pytz

from freezegun import freeze_time
from datetime import datetime

from src.common.logger import Logger


class TestLogger:

    @staticmethod
    def test_log_file_has_correct_info_if_info_messages_with_log_filename_are_logged() -> None:
        frozen_datetime = datetime(2022, 10, 22, 8, 0, 0,
                                   tzinfo=pytz.timezone('America/Los_Angeles'))

        with freeze_time(frozen_datetime):
            logger = Logger('test_logger')

            logger.log.info("Iniciando teste de log...")
            logger.log.info(f"Gerado arquivo de log {logger.log_file_name}.")

            with open(logger.log_file_name, 'r') as log_file_name:
                log_content = log_file_name.read()

        assert '2022-10-22 12:53:00,000 - test_logger - INFO - Iniciando teste de log...' in log_content and \
               'test_logger-2022-10-22.log.' in log_content

    @staticmethod
    def test_log_file_has_correct_info_if_messages_with_info_warning_and_exception_are_logged() -> None:
        frozen_datetime = datetime(2022, 10, 23, 9, 0, 0,
                                   tzinfo=pytz.timezone('America/Los_Angeles'))
        expected_messages = "2022-10-23 13:53:00,000 - test_logger - INFO - Iniciando teste de log...\n" \
                            "2022-10-23 13:53:00,000 - test_logger - WARNING - Gerado aviso de teste.\n" \
                            "2022-10-23 13:53:00,000 - test_logger - ERROR - Gerada exceÃ§Ã£o de teste.\n" \
                            "KeyError: 'a'\n"

        with freeze_time(frozen_datetime):
            logger = Logger('test_logger')

            logger.log.info("Iniciando teste de log...")
            logger.log.warning(f"Gerado aviso de teste.")
            logger.log.exception(f"Gerada exceção de teste.", exc_info=KeyError('a'))

            with open(logger.log_file_name, 'r') as log_file_name:
                log_content = log_file_name.read()

        assert expected_messages in log_content
