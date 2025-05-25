
# Telegram Bot Service

## Описание

Это проект Telegram-бота и админ-панели на Django, упакованный в Docker.  
---

## Быстрый старт

1. Скопируйте репозиторий:

```bash
git clone https://github.com/Maruf995/Telegram_django.git
cd bot_service/bot_panel
```
2. Сделать миграции:
```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate

3. Создать суперпользователя:
```
docker-compose run web python manage.py createsuperuser
```

4. Создайте файл `.env` на основе файла `.env.example` и заполните его переменные:

```env
BOT_TOKEN=
DB_HOST=
DB_NAME=
DB_USER=
DB_PASS=
DB_PORT=
SECRET_KEY=
```

5. Запустите контейнер Docker:

```bash
docker-compose up -d --build
```
