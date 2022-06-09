import random
import string

import pytest

from psycopg2 import connect
from psycopg2.extensions import connection as Connection


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


class History:
    def __init__(self):
        self.history: list[str] = []

    def __getitem__(self, item: str):
        return self.history[int(item)]

    def append(self, item: str):
        self.history.append(item)


class RandomTablenameGenerator:
    def __init__(self, alphabet: str, size: int):
        self.alphabet = alphabet
        self.size = size
        self.history = History()

    @property
    def next(self):
        tablename = "".join(random.choice(string.ascii_lowercase) for _ in range(self.size))
        self.history.append(tablename)
        return tablename


@pytest.fixture
def random_tablename():
    yield RandomTablenameGenerator(string.ascii_lowercase, 16)
