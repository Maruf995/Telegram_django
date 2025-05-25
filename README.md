
# Telegram Bot Service

## Описание

Это проект Telegram-бота и админ-панели на Django, упакованный в Docker.  
---

## Быстрый старт

1. Скопируйте репозиторий:

```bash
git clone <URL_репозитория>
cd <имя_папки_репозитория>
```

2. Создайте файл `.env` на основе файла `.env.example` и заполните его переменные:

```env
BOT_TOKEN=
DB_HOST=
DB_NAME=
DB_USER=
DB_PASS=
DB_PORT=
SECRET_KEY=
```

3. Перейдите в папку с ботом и админ-панелью:

```bash
cd bot_service/bot_panel
```

4. Запустите контейнер Docker:

```bash
docker-compose up -d --build
```
