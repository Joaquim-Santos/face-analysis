import boto3

from typing import List, Union


class S3Service:
    def __init__(self) -> None:
        self.__s3_client = boto3.client("s3")

    def get_files_names(self, bucket: str, prefix: str) -> List[str]:
        response = self.__s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)

        content = response.get("Contents", [])[1:]

        return [item["Key"] for item in content]

    def save_data(self, bucket: str, key: str, data: Union[bytes, str]) -> None:
        self.__s3_client.put_object(Bucket=bucket, Key=key, Body=data)
