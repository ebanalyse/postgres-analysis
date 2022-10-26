import string
import os
import pytest
import datetime
from psycopg2 import connect
from psycopg2.extensions import connection as Connection

from tests.utils import RandomTablenameGenerator


@pytest.fixture
def postgres_connection():
    connection: Connection

    with connect(dbname="postgres", user="postgres", port=5432, host="localhost", password="postgres") as connection:
        yield connection


@pytest.fixture
def random_tablename():
    yield RandomTablenameGenerator(string.ascii_lowercase, 16)


@pytest.fixture(autouse=True, scope="session")
def test_run_start_time():
    test_start_time = set_test_start_time()
    print(test_start_time)
    return test_start_time


def set_test_start_time():
    return datetime.datetime.today().strftime("%Y-%m-%dT%H-%M")


def pytest_sessionstart(session):
    os.mkdir("./results/" + set_test_start_time())
