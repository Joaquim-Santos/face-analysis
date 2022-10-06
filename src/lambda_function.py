from typing import List, Dict, Union

from src.face_analysis import FaceAnalysis


def lambda_handler(event: dict, context) -> List[Dict[str, Union[str, float]]]:
    return FaceAnalysis(event).detect_faces()


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
