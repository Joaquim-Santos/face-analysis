from src.services.face_analysis import FaceAnalysis
from common.exceptions.abstract_exception import AbstractException


def lambda_handler(event: dict, context) -> dict:
    try:
        detected_images = FaceAnalysis(event).detect_faces()

        return {
            'statusCode': 200,
            'body': f'Detectada(s) {len(detected_images)} imagem(ns).'
        }
    except AbstractException as detected_error:
        return {
            'statusCode': detected_error.status_code,
            'body': detected_error.message
        }


if __name__ == "__main__":
    local_event = {
        'Records': [
            {
                'eventVersion': '2.1',
                'eventSource': 'aws: s3',
                'awsRegion': 'us-east-1',
                'eventTime': '2022-10-06T16: 45: 29.984Z',
                'eventName': 'ObjectCreated: Put',
                's3': {
                    's3SchemaVersion': '1.0',
                    'configurationId': 'fbf34c6f-d2a4-4d9b-be64-3672e240cfd8',
                    'bucket': {
                        'name': 'face-analysis-images',
                        'ownerIdentity': {
                            'principalId': 'A2ZR7ZFKTEA4FJ'
                        },
                        'arn': 'arn: aws: s3: : : face-analysis-images'
                    },
                    'object': {
                        'key': 'output/winchester_family.png',
                        'size': 562392,
                        'eTag': '97edcbdb5aa7506ebceec6c51dabf5b1',
                        'sequencer': '00633F0629DE07533F'
                    }
                }
            }
        ]
    }

    result = lambda_handler(local_event, {})
    print(result)
