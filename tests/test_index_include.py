import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        # content_id first
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 10000) AS content_id, gen_random_uuid() AS user_id FROM generate_series(1, 10000000)",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 10000) AS content_id, gen_random_uuid() AS user_id FROM generate_series(1, 10000000)",
            "CREATE INDEX ON {tablename.history[-1]} (content_id)",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 10000) AS content_id, gen_random_uuid() AS user_id FROM generate_series(1, 10000000)",
            "CREATE INDEX ON {tablename.history[-1]} (content_id, user_id)",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 10000) AS content_id, gen_random_uuid() AS user_id FROM generate_series(1, 10000000)",
            "CREATE INDEX ON {tablename.history[-1]} (content_id) INCLUDE (user_id)",
        ],
        # user_id first
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT gen_random_uuid() AS user_id, ROUND(RANDOM() * 10000) AS content_id FROM generate_series(1, 10000000)",
            "CREATE INDEX ON {tablename.history[-1]} (user_id)",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT gen_random_uuid() AS user_id, ROUND(RANDOM() * 10000) AS content_id FROM generate_series(1, 10000000)",
            "CREATE INDEX ON {tablename.history[-1]} (user_id, content_id)",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT gen_random_uuid() AS user_id, ROUND(RANDOM() * 10000) AS content_id FROM generate_series(1, 10000000)",
            "CREATE INDEX ON {tablename.history[-1]} (user_id) INCLUDE (content_id)",
        ],
    ],
)
def test_performance(
    postgres_connection, random_tablename: str, statements: str | list[str]
):
    execute_and_measure(
        postgres_connection,
        random_tablename,
        (
            statements
            + ["SELECT user_id FROM {tablename.history[-1]} WHERE content_id = 5000"]
        ),
    )
