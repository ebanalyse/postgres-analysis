import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        # SELECT FROM table partition
        [
            "CREATE TABLE {tablename.next} (partition_id INT NOT NULL, user_id INT NOT NULL, PRIMARY KEY (partition_id, user_id)) PARTITION BY LIST(partition_id)",
            "CREATE TABLE {tablename.next} PARTITION OF {tablename.first} FOR VALUES IN (1)",
            "INSERT INTO {tablename.first} (partition_id, user_id) SELECT 1 AS partition_id, generate_series AS user_id FROM generate_series(1, 10000)",
            "SELECT user_id FROM {tablename.previous}",
            "ALTER TABLE {tablename.first} RENAME COLUMN user_id TO user_id_int",
        ],
    ],
)
def test_performance(postgres_connection, random_tablename: str, statements: str | list[str], test_run_start_time):
    execute_and_measure(postgres_connection, random_tablename, statements, __file__, test_run_start_time)
