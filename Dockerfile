FROM python:3.11-slim

RUN apt-get update \
    && apt-get -y install libmariadb-dev gcc python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app/bot

COPY requirements.txt /usr/src/app/bot

RUN pip install --no-cache-dir -r /usr/src/app/bot/requirements.txt

COPY . /usr/src/app/bot