from src.image_index import ImageIndex


class FaceAnalysis:
    def __init__(self) -> None:
        self.__image_index = ImageIndex()

    def detect_faces(self):
        found_images = self.__image_index.match_images('winchester_family.png')
        print(found_images)


if __name__ == "__main__":
    FaceAnalysis().detect_faces()
