#!/bin/sh
# entrypoint.sh

echo "Запускаем Django..."
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &

echo "Запускаем Telegram-бота..."
python main.py
