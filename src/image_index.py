import boto3

from typing import List


class ImageIndex:
    def __init__(self) -> None:
        self.__s3 = boto3.resource('s3')
        self.__rekognition_client = boto3.client('rekognition')

    def list_images(self) -> List[str]:
        face_images = []
        bucket = self.__s3.Bucket('face-analysis-images')

        for image in bucket.objects.all():
            face_images.append(image.key)

        return face_images

    def index_collection(self, face_images: List[str]) -> List[dict]:
        detected_faces = []

        for image in face_images:
            face = self.__rekognition_client.index_faces(
                CollectionId='faces',
                Image={
                    'S3Object': {
                        'Bucket': 'face-analysis-images',
                        'Name': image
                    }
                },
                ExternalImageId=image.split('.')[0],
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
                    'Name': "_target.png"
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
