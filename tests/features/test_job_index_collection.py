import time

from mock import patch
from mock.mock import MagicMock

from src.job_index_collection import JobIndexCollection
from src.services.s3_service import S3Service
from src.common.constants import FACES_BUCKET, FACES_BUCKET_INPUT_PREFIX


class TestJobIndexCollection:

    @staticmethod
    def test_job_finished_with_success_if_all_images_on_bucket_are_indexed() -> None:
        job = JobIndexCollection()
        job.start()

        assert (job.success, job.number_of_indexed_images, job.retries) == (True, 4, 0)

    @staticmethod
    @patch.object(S3Service, 'get_files_names')
    def test_job_finished_with_success_if_bucket_has_no_images_to_index(fake_get_files_names: MagicMock) -> None:
        fake_get_files_names.return_value = []

        job = JobIndexCollection()
        job.start()

        assert (job.success, job.number_of_indexed_images, job.retries) == (True, 0, 0)

    @staticmethod
    @patch.object(time, 'sleep')
    def test_job_finished_with_success_if_has_one_retry_after_client_error(fake_sleep: MagicMock) -> None:

        fake_sleep.call_args = 1
        all_files = S3Service().get_files_names(FACES_BUCKET, FACES_BUCKET_INPUT_PREFIX)

        with patch.object(S3Service, 'get_files_names') as fake_get_files_names:
            fake_get_files_names.side_effect = [
                ['input/fake_image.png'],
                all_files
            ]

            job = JobIndexCollection()
            job.start()

        assert (job.success, job.number_of_indexed_images, job.retries) == (True, 4, 1)

    @staticmethod
    @patch.object(S3Service, 'get_files_names')
    @patch.object(time, 'sleep')
    def test_job_failed_if_exceed_max_retries_due_generic_error(
            fake_sleep: MagicMock, fake_get_files_names: MagicMock) -> None:

        fake_sleep.call_args = 1
        fake_get_files_names.return_value = ['fake_image.png']

        job = JobIndexCollection()
        job.start()

        assert (job.success, job.number_of_indexed_images, job.retries) == (False, 0, 6)
