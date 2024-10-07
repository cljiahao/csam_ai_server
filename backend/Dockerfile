ARG PYTHON=python:3.11.10-slim

# Base image with shared configurations
FROM $PYTHON AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /api
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./src ./src
WORKDIR /api/src
CMD ["sh", "-c", "python main.py"]