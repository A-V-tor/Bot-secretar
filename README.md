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
  AUTHORIZATION_KEY - ключ для для запросов к API # должен совпадать со знчением "authorizationKey"
  ```

- по пути `project/adminpanel/static/admin/js` создать файл `.env.json` по аналогии с `env.json.example`
  ```
  {
    "notesUrl": "http://localhost:5000/all-notes" //  ендпоинт заметок
    "authorizationKey": "1234567" //  ключ для для запросов к API # должен совпадать со знчением "AUTHORIZATION_KEY"
  }
  ```
- Создание виртуального окружения и установка заисимотей
  ```
  poetry shell
  poetry install
  ```
- Создание и приминение минраций к бд
  ```
  alembic revision --autogenerate -m "initial revision"
  alembic upgrade head
  ```
  Локальный запуск для разработки через `developers_manager.py` 
