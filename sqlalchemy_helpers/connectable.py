import logging
import time
from contextlib import contextmanager
from typing import (Union,
                    Generator)

from sqlalchemy.engine import (Connection,
                               Engine,
                               create_engine)
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import (Session,
                            sessionmaker)

DbUriType = Union[str, URL]


@contextmanager
def get_engine(db_uri: DbUriType,
               *,
               case_sensitive=True,
               encoding='utf-8',
               echo=False
               ) -> Generator[Engine, None, None]:
    engine = create_engine(db_uri,
                           case_sensitive=case_sensitive,
                           echo=echo,
                           encoding=encoding)
    try:
        yield engine
    finally:
        engine.dispose()


@contextmanager
def get_connection(engine: Engine
                   ) -> Generator[Connection, None, None]:
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def get_session(engine: Engine,
                *,
                auto_flush: bool = True,
                auto_commit: bool = False,
                expire_on_commit: bool = True
                ) -> Generator[Session, None, None]:
    session_factory = sessionmaker(bind=engine,
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
                     retry_interval: int = 2
                     ) -> None:
    db_uri_str = db_uri_to_str(db_uri)
    logging.info('Establishing connection '
                 f'with "{db_uri_str}".')
    with get_engine(db_uri) as engine:
        for attempt_num in range(retry_attempts):
            try:
                connection = engine.connect()
                connection.close()
                break
            except OperationalError:
                err_msg = ('Connection attempt '
                           f'#{attempt_num + 1} failed.')
                logging.error(err_msg)
                time.sleep(retry_interval)
        else:
            err_message = ('Failed to establish connection '
                           f'with "{db_uri_str}" '
                           f'after {retry_attempts} attempts '
                           f'with {retry_interval} s. interval.')
            raise ConnectionError(err_message)

    logging.info(f'Connection established with "{db_uri_str}".')


def db_uri_to_str(db_uri: DbUriType) -> str:
    try:
        return db_uri.__to_string__()
    except AttributeError:
        return str(db_uri)
