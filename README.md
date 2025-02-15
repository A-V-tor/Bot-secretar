<h1 align="center">Личный бот - секретарь</h1>
<br>
<div id="header" align="center">
<img src='https://media.giphy.com/media/wlR4kWTnwEyY8RwHKM/giphy.gif' width="100"/>
</div>

<div id="header" align="center">
<h5 align="center"><img src="https://github.com/A-V-tor/Bot-secretar/blob/main/assets/bot.png"></h5>
</div>


## Настройка и запуск
- <добавить инфу>

  ```
- Создание виртуального окружения и установка зависимостей
  ```
  poetry shell
  poetry install
  ```

- Создание и применение миграций к бд
  ```
  alembic revision --autogenerate -m "initial revision"
  alembic upgrade head
  ```

## Pre commit
Включить в работу `pre-commit install` </br>
Проверка создания файла `cat .git/hooks/pre-commit` </br>
Проверка согласно конфигурации `pre-commit run --all-files` </br>
