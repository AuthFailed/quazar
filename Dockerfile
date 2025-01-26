FROM python:3.11-slim

RUN apt-get update \
    && apt-get -y install libmariadb-dev gcc \

WORKDIR /usr/src/app/bot

COPY requirements.txt /usr/src/app/bot

RUN pip install -r /usr/src/app/bot/requirements.txt

COPY . /usr/src/app/bot
