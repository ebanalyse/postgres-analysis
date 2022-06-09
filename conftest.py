import string

import pytest

from psycopg2 import connect
from psycopg2.extensions import connection as Connection

from tests.utils import RandomTablenameGenerator


@pytest.fixture
def postgres_connection():
    connection: Connection

    with connect(
        dbname="postgres",
        user="postgres",
        port=5432,
        host="localhost",
    ) as connection:
        yield connection


@pytest.fixture
def random_tablename():
    yield RandomTablenameGenerator(string.ascii_lowercase, 16)
