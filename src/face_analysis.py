from typing import List, Dict, Union

from src.logger import Logger
from src.image_index import ImageIndex
from src.exceptions import BadRequest


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

        return self.__image_index.match_images(self.__image_name)
