from contextlib import _GeneratorContextManager

import pytest
import sqlalchemy.exc
from sqlalchemy.engine import (Engine,
                               Connection)
from sqlalchemy.orm import Session
from sqlalchemy.sql import ClauseElement

from sqlalchemy_helpers.connectable import (DbUriType,
                                            create_engine,
                                            open_connection,
                                            open_session, db_uri_to_str,
                                            check_connection)
from tests.utils import is_context_manager, is_non_empty_string


def test_create_engine(db_uri: DbUriType,
                       statement: ClauseElement,
                       statement_result: int) -> None:
    context_manager = create_engine(db_uri)
    with context_manager as engine:
        result = engine.scalar(statement)

    assert isinstance(context_manager, _GeneratorContextManager)
    assert isinstance(engine, Engine)
    assert is_context_manager(context_manager)
    assert result == statement_result


def test_open_connection(engine: Engine,
                         statement: ClauseElement,
                         statement_result: int) -> None:
    context_manager = open_connection(engine)
    with context_manager as connection:
        result = connection.scalar(statement)

    assert isinstance(context_manager, _GeneratorContextManager)
    assert isinstance(connection, Connection)
    assert is_context_manager(context_manager)
    assert result == statement_result

    with pytest.raises(sqlalchemy.exc.StatementError):
        connection.scalar(statement)


def test_open_session(engine: Engine,
                      statement: ClauseElement,
                      statement_result: int) -> None:
    context_manager = open_session(engine)
    with context_manager as session:
        result = session.scalar(statement)

    assert isinstance(context_manager, _GeneratorContextManager)
    assert isinstance(session, Session)
    assert is_context_manager(context_manager)
    assert result == statement_result


def test_check_connection(db_uri: DbUriType,
                          nonexistent_db_uri: DbUriType,
                          invalid_db_uri: str) -> None:
    response = check_connection(db_uri)

    assert response is None

    with pytest.raises(ConnectionError):
        check_connection(db_uri,
                         retry_attempts=0)
    with pytest.raises(ConnectionError):
        check_connection(nonexistent_db_uri,
                         retry_interval=0)
    with pytest.raises(sqlalchemy.exc.ArgumentError):
        check_connection(invalid_db_uri)


def test_db_uri_to_str(db_uri: DbUriType) -> None:
    db_uri_str = db_uri_to_str(db_uri)

    assert is_non_empty_string(db_uri_str)
