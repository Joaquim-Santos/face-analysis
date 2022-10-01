from typing import List, Dict, Union

from src.image_index import ImageIndex


class FaceAnalysis:
    def __init__(self) -> None:
        self.__image_index = ImageIndex()

    def detect_faces(self) -> List[Dict[str, Union[str, float]]]:
        return self.__image_index.match_images('winchester_family.png')


if __name__ == "__main__":
    found_images = FaceAnalysis().detect_faces()
    print(found_images)
