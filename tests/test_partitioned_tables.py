import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        # SELECT FROM table partition
        [
            "CREATE TABLE {tablename.next} (partition_id INT NOT NULL, user_id INT NOT NULL, PRIMARY KEY (partition_id, user_id)) PARTITION BY LIST(partition_id)",
            "CREATE TABLE {tablename.next} PARTITION OF {tablename.first} FOR VALUES IN (1)",
            "INSERT INTO {tablename.first} (partition_id, user_id) SELECT 1 AS partition_id, generate_series AS user_id FROM generate_series(1, 1000000)",
            "SELECT user_id FROM {tablename.previous}",
        ],
        [
            "CREATE TABLE {tablename.next} (user_id INT NOT NULL, partition_id INT NOT NULL, PRIMARY KEY (user_id, partition_id)) PARTITION BY LIST(partition_id)",
            "CREATE TABLE {tablename.next} PARTITION OF {tablename.first} FOR VALUES IN (1)",
            "INSERT INTO {tablename.first} (user_id, partition_id) SELECT generate_series AS user_id, 1 AS partition_id FROM generate_series(1, 1000000)",
            "SELECT user_id FROM {tablename.previous}",
        ],
        # SELECT FROM partitioned table
        [
            "CREATE TABLE {tablename.next} (partition_id INT NOT NULL, user_id INT NOT NULL, PRIMARY KEY (partition_id, user_id)) PARTITION BY LIST(partition_id)",
            "CREATE TABLE {tablename.next} PARTITION OF {tablename.first} FOR VALUES IN (1)",
            "INSERT INTO {tablename.first} (partition_id, user_id) SELECT 1 AS partition_id, generate_series AS user_id FROM generate_series(1, 1000000)",
            "SELECT user_id FROM {tablename.first} WHERE partition_id = 1",
        ],
        [
            "CREATE TABLE {tablename.next} (user_id INT NOT NULL, partition_id INT NOT NULL, PRIMARY KEY (user_id, partition_id)) PARTITION BY LIST(partition_id)",
            "CREATE TABLE {tablename.next} PARTITION OF {tablename.first} FOR VALUES IN (1)",
            "INSERT INTO {tablename.first} (user_id, partition_id) SELECT generate_series AS user_id, 1 AS partition_id FROM generate_series(1, 1000000)",
            "SELECT user_id FROM {tablename.first} WHERE partition_id = 1",
        ],
    ],
)
def test_performance(
    postgres_connection, random_tablename: str, statements: str | list[str]
):
    execute_and_measure(
        postgres_connection,
        random_tablename,
        statements,
    )
