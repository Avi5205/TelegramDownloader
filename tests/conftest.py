import pytest

from database.initializer import initialize_database


@pytest.fixture(scope="session", autouse=True)
def initialize_test_database():
    initialize_database()
