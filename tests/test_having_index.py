import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 50000) AS user_id, ('{{ekstrabladet,jyllandsposten,politiken}}'::TEXT[])[ROUND(RANDOM() * 2)] AS platform FROM generate_series(1, 10000000)",
            "SELECT user_id FROM {tablename.history[-1]} GROUP BY user_id HAVING COUNT(*) FILTER (WHERE platform = 'ekstrabladet') > 2",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 50000) AS user_id, ('{{ekstrabladet,jyllandsposten,politiken}}'::TEXT[])[ROUND(RANDOM() * 2)] AS platform FROM generate_series(1, 10000000)",
            "CREATE INDEX ON {tablename.history[-1]} (platform, user_id)",
            "SELECT user_id FROM {tablename.history[-1]} GROUP BY user_id HAVING COUNT(*) FILTER (WHERE platform = 'ekstrabladet') > 2",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 50000) AS user_id, ('{{ekstrabladet,jyllandsposten,politiken}}'::TEXT[])[ROUND(RANDOM() * 2)] AS platform FROM generate_series(1, 10000000)",
            "CREATE INDEX ON {tablename.history[-1]} (user_id, platform)",
            "SELECT user_id FROM {tablename.history[-1]} GROUP BY user_id HAVING COUNT(*) FILTER (WHERE platform = 'ekstrabladet') > 2",
        ],
        # materialized view
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 50000) AS user_id, ('{{ekstrabladet,jyllandsposten,politiken}}'::TEXT[])[ROUND(RANDOM() * 2)] AS platform FROM generate_series(1, 10000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT platform, user_id, COUNT(*) AS count FROM {tablename.history[-2]} GROUP BY platform, user_id",
            "SELECT user_id FROM {tablename.history[-1]} WHERE platform = 'ekstrabladet' AND count > 2",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 50000) AS user_id, ('{{ekstrabladet,jyllandsposten,politiken}}'::TEXT[])[ROUND(RANDOM() * 2)] AS platform FROM generate_series(1, 10000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT platform, user_id, COUNT(*) AS count FROM {tablename.history[-2]} GROUP BY platform, user_id",
            "CREATE INDEX ON {tablename.history[-1]} (platform, user_id) INCLUDE (count)",
            "SELECT user_id FROM {tablename.history[-1]} WHERE platform = 'ekstrabladet' AND count > 2",
        ],
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 50000) AS user_id, ('{{ekstrabladet,jyllandsposten,politiken}}'::TEXT[])[ROUND(RANDOM() * 2)] AS platform FROM generate_series(1, 10000000)",
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT platform, user_id, COUNT(*) AS count FROM {tablename.history[-2]} GROUP BY platform, user_id",
            "CREATE INDEX ON {tablename.history[-1]} (platform, count) INCLUDE (user_id)",
            "SELECT user_id FROM {tablename.history[-1]} WHERE platform = 'ekstrabladet' AND count > 2",
        ],
    ],
)
def test_performance(postgres_connection, random_tablename: str, statements: str | list[str], test_run_start_time):
    execute_and_measure(postgres_connection, random_tablename, statements, __file__, test_run_start_time)
