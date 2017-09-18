import pytest
from sqlalchemy_utils import (database_exists,
                              create_database,
                              drop_database)

from sqlalchemy_helpers.connectable import DbUriType
from tests import strategies
from tests.utils import example


@pytest.fixture(scope='function')
def db_uri() -> DbUriType:
    result = example(strategies.db_uris)
    if not database_exists(result):
        create_database(result)
    try:
        yield result
    finally:
        drop_database(result)


@pytest.fixture(scope='function')
def nonexistent_db_uri() -> DbUriType:
    while True:
        result = example(strategies.db_uris)
        if database_exists(result):
            continue
        return result


@pytest.fixture(scope='function')
def invalid_db_uri() -> str:
    return example(strategies.invalid_db_uris)
