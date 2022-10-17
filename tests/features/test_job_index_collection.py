import os
import time

from mock import patch
from mock.mock import MagicMock

from src.job_index_collection import JobIndexCollection
from src.services.s3_service import S3Service


class TestJobIndexCollection:

    @staticmethod
    def test_job_finished_with_success_if_all_images_on_bucket_are_indexed() -> None:
        job = JobIndexCollection()
        job.start()

        assert (job.success, job.number_of_indexed_images, 0) == (True, 4, job.retries)

    @staticmethod
    @patch.object(S3Service, 'get_files_names')
    @patch.object(time, 'sleep')
    def test_job_finished_with_success_if_has_one_retry_after_client_error(
            fake_sleep: MagicMock,
            fake_get_files_names: MagicMock) -> None:

        fake_sleep.call_args = 1
        fake_get_files_names.side_effect = [
            ['input/fake_image.png'],
            S3Service.get_files_names
        ]

        job = JobIndexCollection()
        job.start()

        assert (job.success, job.number_of_indexed_images, 1) == (True, 4, job.retries)
