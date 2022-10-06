from typing import List, Dict, Union
from botocore.exceptions import ClientError

from src.logger import Logger
from src.services.image_index import ImageIndex
from src.exceptions import BadRequest, GenericException


class FaceAnalysis:

    def __init__(self, event: dict) -> None:
        self.__image_name: str

        self.__logger = Logger('face_analysis')
        self.__image_index = ImageIndex()

        self.__set_image_name(event)

    def __set_image_name(self, event: dict) -> None:
        self.__logger.log.info(f"Evento recebido: {event}")

        try:
            self.__image_name = event['Records'][0]['s3']['object']['key']
        except (KeyError, IndexError) as error:
            message = f"Evento recebido não possui campos necessários: {error}"

            self.__logger.log.exception(message, exc_info=error)
            raise BadRequest(message, payload={'error': str(error)})

    def detect_faces(self) -> List[Dict[str, Union[str, float]]]:
        self.__logger.log.info(f"Iniciada detecção de faces para imagem: {self.__image_name}")

        try:
            detected_images = self.__image_index.match_images(self.__image_name)

            self.__logger.log.info(f"Detecção de faces finalizada com sucesso.\n"
                                   f"Detectado: {detected_images}")
            return detected_images
        except ClientError as client_error:
            message = f"Erro ao chamar serviços AWS para detecção de faces: " \
                      f"{client_error.response['Error']['Message']}"

            self.__logger.log.exception(message, exc_info=client_error)
            raise GenericException(
                message=message,
                status_code=client_error.response['ResponseMetadata']['HTTPStatusCode'],
                payload={'client_error': message}
            )
        except Exception as generic_error:
            message = f"Erro desconhecido durante detecção de faces: {generic_error}"

            self.__logger.log.exception(message, exc_info=generic_error)
            raise GenericException(
                message=message, status_code=500,
                payload={'generic_error': message}
            )
