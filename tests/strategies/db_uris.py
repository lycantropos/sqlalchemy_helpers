import os
import string

from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy
from sqlalchemy.engine.url import (URL,
                                   make_url)

from sqlalchemy_helpers.config import MAX_IDENTIFIER_LENGTH

postgres_uri_sample = make_url(os.environ['POSTGRES_URI'])
mysql_uri_sample = make_url(os.environ['MYSQL_URI'])

identifiers_characters = strategies.characters(min_codepoint=ord('a'),
                                               max_codepoint=ord('z'))
identifiers = strategies.text(alphabet=identifiers_characters,
                              min_size=8,
                              max_size=MAX_IDENTIFIER_LENGTH)


def db_uris_factory(db_uri_sample: URL) -> SearchStrategy:
    return strategies.builds(
            URL,
            drivername=strategies.just(db_uri_sample.drivername),
            username=strategies.just(db_uri_sample.username),
            password=strategies.just(db_uri_sample.password),
            host=strategies.just(db_uri_sample.host),
            port=strategies.just(db_uri_sample.port),
            database=identifiers,
            query=strategies.just(db_uri_sample.query))


postgres_uris = db_uris_factory(postgres_uri_sample)
mysql_uris = db_uris_factory(mysql_uri_sample)
db_uris = strategies.one_of(postgres_uris,
                            mysql_uris)
invalid_db_uris_characters = strategies.characters(
        blacklist_characters=string.printable)
invalid_db_uris = strategies.text(alphabet=invalid_db_uris_characters)
