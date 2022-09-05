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
        responses = []

        for image in face_images:
            response = self.__rekognition_client.index_faces(
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

            responses.append(response)

        return responses


if __name__ == "__main__":
    image_index = ImageIndex()

    images = image_index.list_images()
    image_index.index_collection(images)
