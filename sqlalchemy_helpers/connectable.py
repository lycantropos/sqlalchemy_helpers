import logging
import time
from contextlib import contextmanager
from typing import (Union,
                    Generator)

from sqlalchemy.engine import (Connectable,
                               Connection,
                               Engine,
                               create_engine as raw_create_engine)
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import (OperationalError,
                            InternalError)
from sqlalchemy.orm import (Session,
                            sessionmaker)

DbUriType = Union[str, URL]

logger = logging.getLogger('sqlalchemy_helpers')


@contextmanager
def create_engine(db_uri: DbUriType,
                  *,
                  case_sensitive: bool = True,
                  encoding: str = 'utf-8',
                  echo: bool = False
                  ) -> Generator[Engine, None, None]:
    engine = raw_create_engine(db_uri,
                               case_sensitive=case_sensitive,
                               echo=echo,
                               encoding=encoding)
    try:
        yield engine
    finally:
        engine.dispose()


@contextmanager
def open_connection(connectable: Connectable
                    ) -> Generator[Connection, None, None]:
    connection = connectable.connect()
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def open_session(connectable: Connectable,
                 *,
                 auto_flush: bool = True,
                 auto_commit: bool = False,
                 expire_on_commit: bool = True
                 ) -> Generator[Session, None, None]:
    session_factory = sessionmaker(bind=connectable,
                                   autoflush=auto_flush,
                                   autocommit=auto_commit,
                                   expire_on_commit=expire_on_commit)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def check_connection(db_uri: DbUriType,
                     *,
                     retry_attempts: int = 10,
                     retry_interval: int = 2) -> None:
    db_uri_str = db_uri_to_str(db_uri)
    logger.info('Establishing connection '
                'with "{db_uri_str}".'
                .format(db_uri_str=db_uri_str))
    with create_engine(db_uri) as engine:
        for attempt_index in range(1, retry_attempts + 1):
            try:
                connection = engine.connect()
                connection.close()
                break
            except (OperationalError, InternalError):
                err_msg = ('Connection attempt '
                           '#{attempt_index} failed.'
                           .format(attempt_index=attempt_index))
                logger.error(err_msg)
                time.sleep(retry_interval)
        else:
            err_message = ('Failed to establish connection '
                           'with "{db_uri_str}" '
                           'after {retry_attempts} attempts '
                           'with {retry_interval} s. interval.'
                           .format(db_uri_str=db_uri_str,
                                   retry_attempts=retry_attempts,
                                   retry_interval=retry_interval))
            raise ConnectionError(err_message)

    logger.info('Connection established with "{db_uri_str}".'
                .format(db_uri_str=db_uri_str))


def db_uri_to_str(db_uri: DbUriType) -> str:
    try:
        return db_uri.__to_string__()
    except AttributeError:
        return str(db_uri)
