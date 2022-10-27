import pytest

from .utils import execute_and_measure


@pytest.mark.parametrize(
    "statements",
    [
        [
            "CREATE TEMPORARY TABLE {tablename.next} AS SELECT ROUND(RANDOM() * 50000) AS user_id, ('{{ekstrabladet,jyllandsposten,politiken}}'::TEXT[])[ROUND(RANDOM() * 2)] AS platform FROM generate_series(1, 10000000)",
            "CREATE VIEW temp_view AS (SELECT user_id FROM (SELECT user_id, COUNT(*) AS rows FROM {tablename.history[-1]} GROUP BY user_id ORDER BY rows DESC LIMIT 1))",
            "CREATE MATERIALIZED VIEW temp_mat_view AS (SELECT user_id FROM (SELECT user_id, COUNT(*) AS rows FROM {tablename.history[-1]} GROUP BY user_id ORDER BY rows DESC LIMIT 1))",
            "SELECT * FROM temp_view",
            "SELECT * FROM temp_mat_view",
        ],
    ],
)
def test_performance(postgres_connection, random_tablename: str, statements: str | list[str], test_run_start_time):
    execute_and_measure(postgres_connection, random_tablename, statements, __file__, test_run_start_time)
