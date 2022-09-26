import boto3
import os

from typing import List, Dict


class ImageIndex:
    def __init__(self) -> None:
        self.__s3_client = boto3.client('s3')
        self.__bucket = os.environ['FACES_BUCKET']
        self.__input_prefix = 'input/'
        self.__target_image_path = 'output/target.png'

        self.__rekognition_client = boto3.client('rekognition')

    def list_images(self) -> Dict[str, str]:
        face_images = {}

        response = self.__s3_client.list_objects_v2(Bucket=self.__bucket,
                                                    Prefix=self.__input_prefix)

        for item in response['Contents'][1:]:
            image_name = item['Key'].split(self.__input_prefix)[1]
            image_name = image_name.split('.')[0]

            face_images[item['Key']] = image_name

        return face_images

    def index_collection(self, face_images: Dict[str, str]) -> List[dict]:
        detected_faces = []

        for image_path, image_name in face_images.items():
            face = self.__rekognition_client.index_faces(
                CollectionId='faces',
                Image={
                    'S3Object': {
                        'Bucket': 'face-analysis-images',
                        'Name': image_path
                    }
                },
                ExternalImageId=image_name,
                DetectionAttributes=[
                    'DEFAULT'
                ]
            )

            detected_faces.append(face)

        return detected_faces

    def index_target_image(self) -> dict:
        return self.__rekognition_client.index_faces(
            CollectionId='faces',
            Image={
                'S3Object': {
                    'Bucket': 'face-analysis-images',
                    'Name': self.__target_image_path
                }
            },
            ExternalImageId="target",
            DetectionAttributes=[
                'DEFAULT'
            ]
        )


if __name__ == "__main__":
    image_index = ImageIndex()

    images = image_index.list_images()
    image_index.index_collection(images)
