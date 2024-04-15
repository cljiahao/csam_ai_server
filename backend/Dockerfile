FROM python:3.10.14
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY ./src ./src
WORKDIR /api/src
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]