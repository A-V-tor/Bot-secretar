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
- Запуск Celery
  Запуск работника ` celery -A project.telegram worker --loglevel=info` </br>
  Запуск планировщика  ` celery -A project.telegram beat --loglevel=info` </br>
- ## Локальный запуск для разработки через `developers_manager.py` 


## Пример настройки демона Celery
`file /etc/default/celeryd` </br>
```
# The names of the workers. This example create one worker
CELERYD_NODES="worker1"

# The name of the Celery App, should be the same as the python file
# where the Celery tasks are defined
CELERY_APP="project.telegram.tasks:app"

# Log and PID directories
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"

# Log level
CELERYD_LOG_LEVEL=INFO

# Path to celery binary, that is in your virtual environment
CELERY_BIN=/root/Bot-secretar/.venv/bin/celery

# Options for Celery Beat
CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"
```
`file /etc/systemd/system/celeryd.service`
```
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=root
Group=root
EnvironmentFile=/etc/default/celeryd
WorkingDirectory=/root/Bot-secretar
ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

[Install]
WantedBy=multi-user.target
```
`file /etc/systemd/system/celerybeat.service `
```
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=simple
User=root
Group=root
EnvironmentFile=/etc/default/celeryd
WorkingDirectory=/root/Bot-secretar
ExecStart=/bin/sh -c '${CELERY_BIN}  \
  -A ${CELERY_APP} beat --pidfile=${CELERYBEAT_PID_FILE} \
  --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'

[Install]
WantedBy=multi-user.target
```

Логи celery

```
mkdir /var/log/celery /var/run/celery
chown root:root /var/log/celery /var/run/celery
```

```
cat /var/log/celery/beat.log
cat /var/log/celery/worker1.log
```