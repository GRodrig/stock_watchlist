FROM python:3.10-slim
RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get clean


COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY ./src /app
WORKDIR /app
