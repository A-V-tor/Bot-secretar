FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
    && pip install "poetry==1.8.3" --no-cache-dir

RUN poetry install

RUN apt-get update \
    && apt-get install -y vim locales \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8

ENV LANG ru_RU.UTF-8

CMD ["bash", "-c", "poetry run alembic upgrade head && poetry run bot"]
