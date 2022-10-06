from botocore.exceptions import ClientError

from src.logger import Logger
from src.services.image_index import ImageIndex


class JobIndexCollection:

    def __init__(self) -> None:
        self.__logger = Logger('face_analysis')
        self.__image_index = ImageIndex()

    def start(self) -> None:
        self.__logger.log.info(f"Iniciada Execução do Job.")

        try:
            indexed_images = self.__image_index.index_input_images()

            self.__logger.log.info(f"Job finalizado com sucesso.\n"
                                   f"Total de imagens indexadas: {len(indexed_images)}")
        except ClientError as client_error:
            message = f"Erro ao chamar serviços AWS para execução do Job: " \
                      f"{client_error.response['Error']['Message']}"

            self.__logger.log.exception(message, exc_info=client_error)
        except Exception as generic_error:
            message = f"Erro desconhecido durante execução do Job: {generic_error}"

            self.__logger.log.exception(message, exc_info=generic_error)


if __name__ == '__main__':
    JobIndexCollection().start()
