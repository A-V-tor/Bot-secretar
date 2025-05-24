<h1 align="center">Личный бот - секретарь</h1>
<a href="https://codecov.io/github/A-V-tor/Bot-secretar" >
 <img src="https://codecov.io/github/A-V-tor/Bot-secretar/graph/badge.svg?token=65PRUK4GYD"/>
 </a>
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

<a href="https://github.com/A-V-tor/Bot-secretar/blob/main/CHANGELOG.md">Журнал изменений<a/>


## Backlogs

- добавить просмотр/удаление напоминаний из телеграм интерфейса
- добавить выбор важности напоминаний
- нужно будет реализовать повтор напоминаий или прямое снятие для очень важных
- клаву с календарем нужно будет вынести в библиотеку для переиспользования
