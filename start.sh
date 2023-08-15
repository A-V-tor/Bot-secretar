#!/bin/bash

# Обработка сигнала Ctrl+C
trap 'echo "Terminating processes..."; pkill -P $$; exit' SIGINT

# Запуск Flask
gunicorn -b 0.0.0.0:5000 app:app &
#python  app.py &

# Запуск бота
python app_bot.py &

# Ожидание завершения обоих процессов
wait
