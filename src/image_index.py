import boto3
import os

from typing import List, Dict
from botocore.exceptions import ClientError


class ImageIndex:
    def __init__(self) -> None:
        self.__s3_client = boto3.client('s3')
        self.__bucket = os.environ['FACES_BUCKET']
        self.__input_prefix = 'input/'
        self.__output_prefix = 'output/'

        self.__rekognition_client = boto3.client('rekognition')
        self.__collection_id = 'faces'

    def __list_input_images(self) -> Dict[str, str]:
        face_images = {}

        response = self.__s3_client.list_objects_v2(Bucket=self.__bucket,
                                                    Prefix=self.__input_prefix)

        for item in response['Contents'][1:]:
            image_name = item['Key'].split(self.__input_prefix)[1]
            image_name = image_name.split('.')[0]

            face_images[item['Key']] = image_name

        return face_images

    def __clean_collection(self) -> None:
        try:
            self.__rekognition_client.delete_collection(CollectionId=self.__collection_id)
        except ClientError:
            pass

        self.__rekognition_client.create_collection(CollectionId=self.__collection_id)

    def __index_collection(self, face_images: Dict[str, str]) -> List[dict]:
        detected_faces = []

        for image_path, image_name in face_images.items():
            face = self.__rekognition_client.index_faces(
                CollectionId=self.__collection_id,
                Image={
                    'S3Object': {
                        'Bucket': self.__bucket,
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

    def index_input_images(self) -> List[dict]:
        self.__clean_collection()
        input_images = self.__list_input_images()
        return image_index.__index_collection(input_images)

    def __index_target_image(self, image_name: str) -> dict:
        return self.__rekognition_client.index_faces(
            CollectionId=self.__collection_id,
            Image={
                'S3Object': {
                    'Bucket': self.__bucket,
                    'Name': f'{self.__output_prefix}{image_name}'
                }
            },
            ExternalImageId="target",
            DetectionAttributes=[
                'DEFAULT'
            ]
        )

    @classmethod
    def __get_detected_faces_ids(cls, detected_faces: dict) -> List[str]:
        return [record['Face']['FaceId'] for record in detected_faces['FaceRecords']]

    def __find_images_by_similarity(self, detected_faces_ids: List[str],
                                    threshold: float = 90) -> List[str]:
        found_images = []

        for face_id in detected_faces_ids:
            matched_faces = self.__rekognition_client.search_faces(
                CollectionId=self.__collection_id,
                FaceId=face_id,
                MaxFaces=10,
                FaceMatchThreshold=threshold
            )

            for face_match in matched_faces['FaceMatches']:
                if face_match['Face']['ExternalImageId'] != 'target':
                    image_name = face_match['Face']['ExternalImageId']
                    found_images.append(image_name)
                    break

        return found_images

    def __delete_target_images(self, detected_faces_ids: List[str]) -> None:
        self.__rekognition_client.delete_faces(
            CollectionId=self.__collection_id,
            FaceIds=detected_faces_ids
        )

    def match_images(self, image_name: str) -> List[str]:
        detected_faces = self.__index_target_image(image_name)
        detected_faces_ids = self.__get_detected_faces_ids(detected_faces)
        found_images = self.__find_images_by_similarity(detected_faces_ids)
        self.__delete_target_images(detected_faces_ids)

        return found_images


if __name__ == "__main__":
    image_index = ImageIndex()
    image_index.index_input_images()
