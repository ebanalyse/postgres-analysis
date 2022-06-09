import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT round(random() * 1000) id FROM generate_series(1, 1000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT round(random() * 1000) AS id FROM generate_series(1, 1000000)",
            """
            SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]} WHERE {tablename.history[-2]}.id = 250
            UNION
            SELECT {tablename.history[-1]}.id FROM {tablename.history[-1]} WHERE {tablename.history[-1]}.id = 750
            """,
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT round(random() * 1000) id FROM generate_series(1, 1000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT round(random() * 1000) AS id FROM generate_series(1, 1000000)",
            "SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]} WHERE {tablename.history[-2]}.id IN (250, 750)",
        ],
    ],
)
def test_performance(postgres_connection, random_tablename: str, statements: str | list[str]):
    execute_and_measure(postgres_connection, random_tablename, statements)
