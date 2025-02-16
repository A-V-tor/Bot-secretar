FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry install

RUN apt-get update \
    && apt-get install -y vim

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8

ENV LANG ru_RU.UTF-8
