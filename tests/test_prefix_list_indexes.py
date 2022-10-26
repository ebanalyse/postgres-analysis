import csv
from io import StringIO
import pytest

from .utils import RandomTablenameGenerator, execute_and_measure


@pytest.fixture
def csv_buffer(request):
    prefix = ""

    rows = []

    for iteration in range(1_000, 1_100):
        if iteration % 2 == 0:
            suffix = str(iteration)
            if prefix:
                prefix += "_" + suffix
            else:
                prefix = suffix
            rows.append((prefix,))

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerows(rows * 100_000)
    buffer.seek(0)

    @request.addfinalizer
    def finalize():
        buffer.close()

    return buffer


@pytest.mark.parametrize(
    "statements",
    [
        "SELECT * FROM {tablename.history[-1]} WHERE sections LIKE '^([[:digit:]]+_)*1500(_[[:digit:]]+)*$'",
        [
            "CREATE INDEX ON {tablename.history[-1]} USING btree (sections)",
            "SELECT * FROM {tablename.history[-1]} WHERE sections LIKE '^([[:digit:]]+_)*1500(_[[:digit:]]+)*$'",
        ],
    ],
)
def test_btree_performance(
    postgres_connection,
    random_tablename: RandomTablenameGenerator,
    csv_buffer,
    statements: str | list[str],
    test_run_start_time,
):
    tablename = random_tablename.next

    with postgres_connection.cursor() as cursor:
        cursor.execute(f"CREATE TEMPORARY TABLE {tablename} (sections TEXT NOT NULL)")
        cursor.copy_from(
            csv_buffer,
            tablename,
        )

    execute_and_measure(postgres_connection, random_tablename, statements, __file__, test_run_start_time)


@pytest.mark.parametrize(
    "statements",
    [
        "SELECT * FROM {tablename.history[-1]} WHERE sections @@ to_tsquery('english', '1500_:*')",
        [
            "CREATE INDEX ON {tablename.history[-1]} USING gin (sections)",
            "SELECT * FROM {tablename.history[-1]} WHERE sections @@ to_tsquery('english', '1500_:*')",
        ],
    ],
)
def test_tsvector_performance(
    postgres_connection,
    random_tablename: RandomTablenameGenerator,
    csv_buffer,
    statements: str | list[str],
    test_run_start_time,
):
    tablename = random_tablename.next

    with postgres_connection.cursor() as cursor:
        cursor.execute(f"CREATE TEMPORARY TABLE {tablename} (sections TSVECTOR NOT NULL)")
        cursor.copy_from(
            csv_buffer,
            tablename,
        )

    execute_and_measure(postgres_connection, random_tablename, statements, __file__, test_run_start_time)
