import pytest

from src.job_index_collection import JobIndexCollection


@pytest.fixture(scope="class")
def index_collection():
    JobIndexCollection().start()
