#!/bin/bash


# Генерируем случайное имя ревизии
REVISION_NAME=$(date +'%Y%m%d%H%M%S')

# Генерируем миграции
alembic revision --autogenerate -m "Revision $REVISION_NAME"

# Применяем миграции
alembic upgrade head

