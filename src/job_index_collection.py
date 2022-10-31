import time

from botocore.exceptions import ClientError

from common.logger import Logger
from src.services.image_index import ImageIndex


class JobIndexCollection:
    def __init__(self) -> None:
        self.__logger = Logger("job_index_collection")
        self.__image_index = ImageIndex()

        self.__retries = 0
        self.__max_retries = 5
        self.__retry_minutes = 60

        self.__number_of_indexed_images = 0
        self.__success = False

    @property
    def number_of_indexed_images(self) -> int:
        return self.__number_of_indexed_images

    @property
    def success(self) -> bool:
        return self.__success

    @property
    def retries(self) -> int:
        return self.__retries

    def __retry(self) -> None:
        self.__retries += 1

        if self.__retries <= self.__max_retries:
            wait = self.__retries * self.__retry_minutes
            self.__logger.log.warning(
                f"Iniciar retentativa {self.__retries} em "
                f"{wait/self.__retry_minutes} minutos."
            )

            time.sleep(wait)
            self.start()
        else:
            self.__logger.log.warning(
                f"Foram feitas {self.__max_retries} retentativa e o Job não teve sucesso."
            )

    def __index_collection(self) -> None:
        self.__logger.log.info("Iniciada Execução do Job.")

        try:
            indexed_images = self.__image_index.index_input_images()
            self.__success = True
            self.__number_of_indexed_images = len(indexed_images)

            self.__logger.log.info(
                f"Job finalizado com sucesso.\n"
                f"Total de imagens indexadas: {self.__number_of_indexed_images}"
            )
        except ClientError as client_error:
            message = (
                f"Erro ao chamar serviços AWS para execução do Job: "
                f"{client_error.response['Error']['Message']}"
            )

            self.__logger.log.exception(message, exc_info=client_error)
        except Exception as generic_error:
            message = f"Erro desconhecido durante execução do Job: {generic_error}"

            self.__logger.log.exception(message, exc_info=generic_error)

    def start(self) -> None:
        self.__index_collection()

        if not self.__success:
            self.__retry()


if __name__ == "__main__":  # pragma: no cover
    JobIndexCollection().start()
