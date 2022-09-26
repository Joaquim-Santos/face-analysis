from src.image_index import ImageIndex


class FaceAnalysis:
    def __init__(self) -> None:
        self.__image_index = ImageIndex()

    def detect_faces(self):
        detected_faces = self.__image_index.index_target_image()
        print(detected_faces)


if __name__ == "__main__":
    FaceAnalysis().detect_faces()
