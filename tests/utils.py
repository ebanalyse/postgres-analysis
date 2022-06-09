from contextlib import contextmanager
import os

from datetime import datetime


def execute_and_measure(postgres_connection, random_tablename: str, statements: str | list[str]):
    if isinstance(statements, str):
        statements = [statements]

    with postgres_connection.cursor() as cursor:
        with measure(LazyJoinedString("; ", [])) as formatted_statements:
            for statement in statements:
                sql = statement.format(tablename=random_tablename)
                if "select" in sql.lower():
                    sql = "EXPLAIN ANALYZE " + sql
                formatted_statements.items.append(sql)
                with measure(sql):
                    cursor.execute(sql)
                if "explain analyze" in sql.lower():
                    print("\n".join("".join(row) for row in cursor.fetchall()) + "\n")


class LazyJoinedString:
    def __init__(self, joiner: str, items: list[str]):
        self.joiner = joiner
        self.items = items

    def __str__(self):
        return str(self.joiner).join(map(str, self.items))


@contextmanager
def measure(description):
    start = datetime.now()
    yield description
    stop = datetime.now()
    difference = stop - start
    total_seconds = str(difference.total_seconds())
    print(description, "::::", total_seconds, "seconds")
    print("-" * os.get_terminal_size().columns + "\n")
