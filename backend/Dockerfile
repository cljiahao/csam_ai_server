ARG PYTHON=python:3.11.10-slim

# Base image with shared configurations
FROM $PYTHON AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /api
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./src ./src

# Production image
FROM base AS prod
WORKDIR /api/src
ENV API_PORT=8000 \
    ENV_STAGE="prod"
CMD ["sh", "-c", "python main.py"]

# Development image
FROM base AS dev
WORKDIR /api/src
ENV API_PORT=5000 \
    ENV_STAGE="dev"
CMD ["sh", "-c", "python main.py"]