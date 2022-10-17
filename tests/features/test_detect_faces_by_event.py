import pytest

from src.lambda_function import lambda_handler


@pytest.fixture(scope="function", autouse=True)
def upload_image_event() -> dict:
    return {
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
                        'key': 'output/sam_and_ruby.png',
                        'size': 562392,
                        'eTag': '97edcbdb5aa7506ebceec6c51dabf5b1',
                        'sequencer': '00633F0629DE07533F'
                    }
                }
            }
        ]
    }


class TestDetectFacesByEvent:

    @staticmethod
    def test_detect_one_face_if_image_in_event_has_match(upload_image_event: dict) -> None:
        detected_images = lambda_handler(upload_image_event, {})

        assert detected_images == {'statusCode': 200, 'body': 'Detectadas 1 imagens.'}
