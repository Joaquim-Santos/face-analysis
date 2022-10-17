import pytest

from src.job_index_collection import JobIndexCollection


@pytest.fixture(scope="session", autouse=True)
def index_collection():
    JobIndexCollection().start()
