import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        # With or without index
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
    ],
)
def test_performance(postgres_connection, random_tablename: str, statements: str | list[str], test_run_start_time):
    execute_and_measure(postgres_connection, random_tablename, statements, __file__, test_run_start_time)
