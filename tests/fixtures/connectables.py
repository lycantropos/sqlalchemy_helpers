import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL

from sqlalchemy_helpers.connectable import create_engine


@pytest.fixture(scope='function')
def engine(db_uri: URL) -> Engine:
    with create_engine(db_uri) as result:
        yield result
