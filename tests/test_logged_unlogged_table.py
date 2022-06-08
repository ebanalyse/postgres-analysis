import os
from datetime import datetime

import pytest
from psycopg2.extensions import connection as Connection


@pytest.mark.parametrize(
    "statements",
    [
        "CREATE TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
        "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
        "CREATE TABLE {tablename.next} AS SELECT DISTINCT generate_series AS id FROM generate_series(1, 1000000)",
        "CREATE UNLOGGED TABLE {tablename.next} AS SELECT DISTINCT generate_series AS id FROM generate_series(1, 1000000)",
        # With or without index
        [
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        [
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        [
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        [
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE INDEX ON {tablename.history[-1]} (id)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        # With or without primary key
        [
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "ALTER TABLE {tablename.history[-1]} ADD PRIMARY KEY (id)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        [
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "ALTER TABLE {tablename.history[-1]} ADD PRIMARY KEY (id)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
        [
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "ALTER TABLE {tablename.history[-1]} ADD PRIMARY KEY (id)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT generate_series AS id FROM generate_series(1, 1000000)",
            "ALTER TABLE {tablename.history[-1]} ADD PRIMARY KEY (id)",
            "CREATE UNLOGGED TABLE {tablename.next} AS SELECT {tablename.history[-3]}.id FROM {tablename.history[-3]} INTERSECT SELECT {tablename.history[-2]}.id FROM {tablename.history[-2]}",
        ],
    ]
)
def test_performance(postgres_connection: Connection, random_tablename: str, statements: str | list[str]):

    if isinstance(statements, str):
        statements = [statements]

    with postgres_connection.cursor() as cursor:
        start = datetime.now()
        for statement in statements:
            sql = statement.format(tablename=random_tablename)
            if "select" in sql.lower():
                sql = "EXPLAIN ANALYZE " + sql
            print(sql)
            cursor.execute(sql)
            if "explain analyze" in sql.lower():
                print("\n".join("".join(row) for row in cursor.fetchall()) + "\n")
        stop = datetime.now()
        difference = stop - start
        total_seconds = str(difference.total_seconds())
        print("Took", total_seconds, "seconds")
        print("    ", "=" * len(total_seconds))
        print("-" * os.get_terminal_size().columns + "\n")
