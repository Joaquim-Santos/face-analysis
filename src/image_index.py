import boto3

from typing import List


class ImageIndex:
    def __init__(self):
        self.__s3 = boto3.resource('s3')

    def list_images(self) -> List[str]:
        images = []
        bucket = self.__s3.Bucket['face-analysis-images']

        for image in bucket.objects.all():
            images.append(image.key)

        print(images)

        return images


if __name__ == "__main__":
    ImageIndex().list_images()
