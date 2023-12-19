<h1>Личный бот - секретарь</h1>
<br>
<div id="header" align="center">
<img src='https://media.giphy.com/media/wlR4kWTnwEyY8RwHKM/giphy.gif' width="100"/>
</div>

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
- Установка дополнительных технологий
  ```
  https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04-ru # redis Linux
  https://gist.github.com/tomysmile/1b8a321e7c58499ef9f9441b2faa0aa8 # redis MAC OS
  ```
- Создание и применение миграций к бд
  ```
  alembic revision --autogenerate -m "initial revision"
  alembic upgrade head
  ```

  Запуск работника Celery ` celery -A project.telegram worker --loglevel=info`
  Запуск планировщика задачи Celery ` celery -A project.telegram beat --loglevel=info`
  Локальный запуск для разработки через `developers_manager.py` 
