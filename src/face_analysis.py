from typing import List, Dict, Union

from src.image_index import ImageIndex


class FaceAnalysis:
    def __init__(self, event: dict) -> None:
        self.__image_name: str
        self.__image_index = ImageIndex()

        self.__set_image_name(event)

    def __set_image_name(self, event: dict) -> None:
        self.__image_name = event['Records'][0]['s3']['object']['key']

    def detect_faces(self) -> List[Dict[str, Union[str, float]]]:
        return self.__image_index.match_images(self.__image_name)
