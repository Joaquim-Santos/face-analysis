import boto3
import os
import json

from typing import List, Dict, Union
from botocore.exceptions import ClientError

from src.s3_service import S3Service


class ImageIndex:
    def __init__(self) -> None:
        self.__s3_service = S3Service()
        self.__faces_bucket = os.environ['FACES_BUCKET']
        self.__site_bucket = os.environ['SITE_BUCKET']
        self.__input_prefix = 'input/'

        self.__rekognition_client = boto3.client('rekognition')
        self.__collection_id = os.environ['COLLECTION_ID']
        self.__target_image_id = 'target'

    def __list_input_images(self) -> Dict[str, str]:
        face_images = {}

        images_paths = self.__s3_service.get_files_names(
            self.__faces_bucket, self.__input_prefix)

        for image_path in images_paths:
            image_name = image_path.split(self.__input_prefix)[1]
            image_name = image_name.split('.')[0]

            face_images[image_path] = image_name

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
                        'Bucket': self.__faces_bucket,
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
        return self.__index_collection(input_images)

    def __index_target_image(self, image_name: str) -> dict:
        return self.__rekognition_client.index_faces(
            CollectionId=self.__collection_id,
            Image={
                'S3Object': {
                    'Bucket': self.__faces_bucket,
                    'Name': image_name
                }
            },
            ExternalImageId=self.__target_image_id,
            DetectionAttributes=[
                'DEFAULT'
            ]
        )

    @classmethod
    def __get_detected_faces_ids(cls, detected_faces: dict) -> List[str]:
        return [record['Face']['FaceId'] for record in detected_faces['FaceRecords']]

    def __find_images_by_similarity(self, detected_faces_ids: List[str],
                                    threshold: float = 90) -> List[Dict[str, Union[str, float]]]:
        found_images = []

        for face_id in detected_faces_ids:
            matched_faces = self.__rekognition_client.search_faces(
                CollectionId=self.__collection_id,
                FaceId=face_id,
                MaxFaces=10,
                FaceMatchThreshold=threshold
            )

            for face_match in matched_faces['FaceMatches']:
                if face_match['Face']['ExternalImageId'] != self.__target_image_id:
                    similarity = round(face_match['Similarity'], 2)
                    image_name = face_match['Face']['ExternalImageId']

                    found_images.append({
                        'image_name': image_name,
                        'similarity': similarity
                    })
                    break

        return found_images

    def __delete_target_images(self, detected_faces_ids: List[str]) -> None:
        self.__rekognition_client.delete_faces(
            CollectionId=self.__collection_id,
            FaceIds=detected_faces_ids
        )

    def __save_data_on_s3(self, found_images: List[Dict[str, Union[str, float]]]) -> None:
        self.__s3_service.save_data(self.__site_bucket, 'data.json',
                                    json.dumps(found_images))

    def match_images(self, image_name: str) -> List[Dict[str, Union[str, float]]]:
        detected_faces = self.__index_target_image(image_name)
        detected_faces_ids = self.__get_detected_faces_ids(detected_faces)
        found_images = self.__find_images_by_similarity(detected_faces_ids)

        self.__delete_target_images(detected_faces_ids)
        self.__save_data_on_s3(found_images)

        return found_images
