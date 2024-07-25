ARG PYTHON=python:3.10.14-slim

FROM $PYTHON AS prod
WORKDIR /api
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./src ./src
WORKDIR /api/src
CMD uvicorn app:app --host 0.0.0.0 --port $API_PORT

FROM $PYTHON AS dev
WORKDIR /api
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./src ./src
WORKDIR /api/src
CMD uvicorn app:app --host 0.0.0.0 --port $API_PORT --reload