import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        # Without index
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT round(random() * 1000) id FROM generate_series(1, 1000000)",
            """
            SELECT {tablename.history[-1]}.id FROM {tablename.history[-1]} WHERE {tablename.history[-1]}.id = 250
            UNION
            SELECT {tablename.history[-1]}.id FROM {tablename.history[-1]} WHERE {tablename.history[-1]}.id = 750
            """,
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT round(random() * 1000) id FROM generate_series(1, 1000000)",
            "SELECT {tablename.history[-1]}.id FROM {tablename.history[-1]} WHERE {tablename.history[-1]}.id IN (250, 750)",
        ],
        # With index
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT round(random() * 1000) id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            """
            SELECT {tablename.history[-1]}.id FROM {tablename.history[-1]} WHERE {tablename.history[-1]}.id = 250
            UNION
            SELECT {tablename.history[-1]}.id FROM {tablename.history[-1]} WHERE {tablename.history[-1]}.id = 750
            """,
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT round(random() * 1000) id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "SELECT {tablename.history[-1]}.id FROM {tablename.history[-1]} WHERE {tablename.history[-1]}.id IN (250, 750)",
        ],
    ],
)
def test_performance(postgres_connection, random_tablename: str, statements: str | list[str], test_run_start_time):
    execute_and_measure(postgres_connection, random_tablename, statements, __file__, test_run_start_time)
