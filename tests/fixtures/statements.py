import pytest
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.expression import text

from tests import strategies
from tests.utils import example


@pytest.fixture(scope='session')
def statement(statement_result: int) -> ClauseElement:
    return text('SELECT {statement_result}'
                .format(statement_result=statement_result))


@pytest.fixture(scope='session')
def statement_result() -> int:
    return example(strategies.integers)
