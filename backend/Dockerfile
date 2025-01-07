ARG PYTHON=python:3.11.10-slim

# Base image with shared configurations
FROM $PYTHON AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /api
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./src ./src
WORKDIR /api/src

FROM base AS dev
COPY ./.env.dev ./.env.dev
CMD ["sh", "-c", "python main.py --ENV dev"]

FROM base AS stage
COPY ./.env.stage ./.env.stage
CMD ["sh", "-c", "python main.py --ENV stage"]

FROM base AS prod
COPY ./.env.prod ./.env.prod
CMD ["sh", "-c", "python main.py --ENV prod"]
