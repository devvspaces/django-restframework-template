from django.db import connection
from django.conf import settings
from contextlib import contextmanager


@contextmanager
def count_queries():
    default_debug = settings.DEBUG
    settings.DEBUG = True

    start = len(connection.queries)
    yield connection
    end = len(connection.queries)

    print(f"Ran {end - start} queries")
    print("======== Start ===========")
    for query in connection.queries[start:]:
        print("\n", query)
    print("=========  End  ===========")

    settings.DEBUG = default_debug
