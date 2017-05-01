FROM python:3.5

WORKDIR /sqlalchemy_helpers
COPY . /sqlalchemy_helpers/
RUN python3 -m pip install .
