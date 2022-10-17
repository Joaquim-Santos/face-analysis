import pytest

from mock import patch
from mock.mock import MagicMock

from src.lambda_function import lambda_handler
from src.services.image_index import ImageIndex


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

        assert detected_images == {'statusCode': 200, 'body': 'Detectada(s) 1 imagem(ns).'}

    @staticmethod
    def test_detect_many_faces_if_image_in_event_has_multiple_matches(upload_image_event: dict) -> None:
        upload_image_event['Records'][0]['s3']['object']['key'] = 'output/winchester_family.png'
        detected_images = lambda_handler(upload_image_event, {})

        assert detected_images == {'statusCode': 200, 'body': 'Detectada(s) 4 imagem(ns).'}

    @staticmethod
    def test_bad_request_in_detect_faces_if_event_has_no_s3_key(upload_image_event: dict) -> None:
        del upload_image_event['Records'][0]['s3']['object']['key']
        detected_images = lambda_handler(upload_image_event, {})

        assert detected_images == {'statusCode': 400,
                                   'body': "Evento recebido não possui campos necessários: 'key'"}

    @staticmethod
    def test_client_error_in_detect_faces_if_s3_key_does_not_exist(upload_image_event: dict) -> None:
        upload_image_event['Records'][0]['s3']['object']['key'] = 'winchester_family.png'
        detected_images = lambda_handler(upload_image_event, {})

        assert detected_images == {
            'statusCode': 400,
            'body': 'Erro ao chamar serviços AWS para detecção de faces: Unable to get object metadata from S3. '
                    'Check object key, region and/or access permissions.'
        }

    @staticmethod
    @patch.object(ImageIndex, '_ImageIndex__get_detected_faces_ids')
    def test_generic_error_in_detect_faces_if_rekognition_return_has_changed(
            fake_get_detected_faces_ids: MagicMock,
            upload_image_event: dict) -> None:

        fake_get_detected_faces_ids.side_effect = KeyError('FaceId')
        detected_images = lambda_handler(upload_image_event, {})

        assert detected_images == {'statusCode': 500,
                                   'body': "Erro desconhecido durante detecção de faces: 'FaceId'"}
