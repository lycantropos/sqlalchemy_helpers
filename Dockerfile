FROM python:3.5

WORKDIR /opt/sqlalchemy_helpers
COPY . /opt/sqlalchemy_helpers/
RUN python3 -m pip install .
