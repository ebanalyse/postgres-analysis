from contextlib import contextmanager

from datetime import datetime
import os
import random


def execute_and_measure(
    postgres_connection,
    random_tablename: str,
    statements: str | list[str],
    results_filename: str = "",
    test_run_start_time="",
):
    if isinstance(statements, str):
        statements = [statements]

    with postgres_connection.cursor() as cursor:
        with measure(LazyJoinedString("; ", []), results_filename, test_run_start_time) as formatted_statements:

            for statement in statements:
                sql = statement.format(tablename=random_tablename)
                if "select" in sql.lower():
                    sql = "EXPLAIN ANALYZE " + sql
                formatted_statements.items.append(sql)
                print()
                with measure(sql, results_filename, test_run_start_time, write=True):
                    cursor.execute(sql)
                if "explain analyze" in sql.lower():
                    for line in ("".join(row) for row in cursor.fetchall()):
                        print("\t" + line)


class LazyJoinedString:
    def __init__(self, joiner: str, items: list[str]):
        self.joiner = joiner
        self.items = items

    def __str__(self):
        return str(self.joiner).join(map(str, self.items))


@contextmanager
def measure(description, results_file: str, test_run_start_time, write: bool = False):
    start = datetime.now()
    yield description
    stop = datetime.now()
    difference = stop - start
    total_seconds = str(difference.total_seconds())
    print(description, "::::", total_seconds, "seconds")
    if write:
        with open(
            os.getcwd() + "/results/" + test_run_start_time + "/" + results_file.split("/")[-1].split(".")[0] + ".csv",
            "a",
        ) as file:
            file.write(str(str(description) + ";" + total_seconds + "\n"))


class History:
    def __init__(self):
        self.history: list[str] = []

    def __getitem__(self, item: str):
        return self.history[int(item)]

    def append(self, item: str):
        self.history.append(item)


class RandomTablenameGenerator:
    def __init__(self, alphabet: str, size: int):
        self.alphabet = alphabet
        self.size = size
        self.history = History()

    @property
    def first(self):
        return self.history[0]

    @property
    def previous(self):
        return self.history[-1]

    @property
    def next(self):
        tablename = "".join(random.choice(self.alphabet) for _ in range(self.size))
        self.history.append(tablename)
        return tablename
