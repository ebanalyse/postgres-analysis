import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        "CREATE TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
        "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
    ],
)
def test_performance(postgres_connection, random_tablename: str, statements: str | list[str], test_run_start_time):
    execute_and_measure(postgres_connection, random_tablename, statements, __file__, test_run_start_time)
