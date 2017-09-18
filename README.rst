.. contents::


In what follows ``python3`` is an alias for ``python3.5``
or any later version (``python3.6`` and so on).

Installation
------------
Install the latest ``pip`` & ``setuptools`` packages versions

.. code-block:: bash

  python3 -m pip install --upgrade pip setuptools

Release
~~~~~~~
Download and install the latest stable version from ``PyPI`` repository

.. code-block:: bash

  python3 -m pip install --upgrade hypothesis_sqlalchemy

Developer
~~~~~~~~~
Download and install the latest version from ``GitHub`` repository

.. code-block:: bash

  git clone https://github.com/lycantropos/hypothesis_sqlalchemy.git
  cd hypothesis_sqlalchemy
  python3 setup.py install

Usage
-----
Assuming that ``POSTGRES_URI`` environment variable is set
and corresponds to the working database instance:

>>> import os
>>> from sqlalchemy.engine.url import make_url
>>> postgres_uri = make_url(os.environ['POSTGRES_URI'])
>>> from sqlalchemy_helpers.connectable import check_connection
>>> check_connection(postgres_uri)
>>> from sqlalchemy_helpers.connectable import create_engine
>>> with create_engine(postgres_uri) as engine:
...     engine.scalar('SELECT 1')
1
>>> from sqlalchemy_helpers.connectable import open_connection
>>> with create_engine(postgres_uri) as engine:
...     with open_connection(engine) as connection:
...         connection.scalar('SELECT 1')
1

Running tests
-------------
Plain

.. code-block:: bash

    export POSTGRES_URI="postgresql://$POSTGRES_USERNAME:$POSTGRES_PASSWORD@$POSTGRES_HOSTNAME:$POSTGRES_PORT/$POSTGRES_DATABASE"
    export MYSQL_URI="mysql+pymysql://$MYSQL_USERNAME:$MYSQL_PASSWORD@$MYSQL_HOSTNAME:$MYSQL_PORT/$MYSQL_DATABASE"
    python3 setup.py test

where

  - ``$POSTGRES_USERNAME``: PostgreSQL database user name
    (e.g. ``postgres``),
  - ``$POSTGRES_PASSWORD``: PostgreSQL database user password
    (e.g. ``ilovepostgresql``),
  - ``$POSTGRES_HOSTNAME``: PostgreSQL database host
    (e.g. ``localhost``),
  - ``$POSTGRES_PORT``: PostgreSQL database port
    (e.g. ``5432``),
  - ``$POSTGRES_DATABASE``: target PostgreSQL database name
    (e.g. ``testdb``),
  - ``$MYSQL_USERNAME``: MySQL database user name
    (e.g. ``root``),
  - ``$MYSQL_PASSWORD``: MySQL database user password
    (e.g. ``ilovemysql``),
  - ``$MYSQL_HOSTNAME``: MySQL database host
    (e.g. ``localhost``),
  - ``$MYSQL_PORT``: MySQL database port
    (e.g. ``3306``),
  - ``$MYSQL_DATABASE``: target MySQL database name
    (e.g. ``testdb``).


Inside ``Docker`` container with remote debugger

.. code-block:: bash

    ./set-dockerhost.sh docker-compose up
