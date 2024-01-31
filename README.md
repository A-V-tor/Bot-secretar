<h1 align="center">Личный бот - секретарь</h1>
<br>
<div id="header" align="center">
<img src='https://media.giphy.com/media/wlR4kWTnwEyY8RwHKM/giphy.gif' width="100"/>
</div>

<div id="header" align="center">
<h5 align="center"><img src="https://github.com/A-V-tor/Bot-secretar/blob/main/bot.png"></h5>
</div>

<i>
   <h3>Функционал</h3>

  <ul>
    <h4>Телеграм</h4>
    <li>Журнал трат</li>
    <li>Журнал веса</li>
    <li>Журнал тренировок</li>
    <li>Получение напоминаний</li>
  </ul>
  <ul>
    <h4>Web админка</h4>
    <li>Сервис заметок</li>
    <li>Создание напоминаний</li>
    <li>Доступ к моделям базы данных</li>


  </ul>
</i>

## Настройка и запуск
- В корне проекта созать файл .env по аналогу с env.example
  ```
  token - токен от Botfather
  headers - заголовки для запросов (парсинг)
  owner_id -  id телеграм для владельца бота
  URL_ADMIN - url админки
  SECRET_KEY - секретный ключ для сессий
  AUTHORIZATION_KEY - ключ для для запросов к API # должен совпадать со знчением "authorizationKey"  из project/adminpanel/static/admin/js
  REDIS_KEY - ключ авторизации с redis
  CHAT_ID - ID телеграма юзера для отправки напоминаний
  ```

- по пути `project/adminpanel/static/admin/js` создать файл `.env.json` по аналогии с `env.json.example`
  ```
  {
    "notesUrl": "http://localhost:5000/api/all-notes", //  ендпоинт заметок
    "botLogsUrl": "http://localhost:5000/api/bot-logs",
    "flaskLogsUrl": "http://localhost:5000/api/flask-logs",
    "authorizationKey": "1234567" //  ключ для для запросов к API # должен совпадать со значением "AUTHORIZATION_KEY из .env"
  }
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
- Запуск Celery
  Запуск работника `celery -A project.telegram worker --loglevel=info` </br>
  Запуск планировщика  `celery -A project.telegram beat --loglevel=info` </br>
- ## Локальный запуск для разработки через `developers_manager.py`

## Pre commit
Включить в работу `pre-commit install` </br>
Проверка создания файла `cat .git/hooks/pre-commit` </br>
Проверка согласно конфигурации `pre-commit run --all-files` </br>


## Дополнительное описание в [документации](https://github.com/A-V-tor/Bot-secretar/wiki)
