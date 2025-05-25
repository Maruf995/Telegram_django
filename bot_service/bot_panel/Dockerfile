FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Устанавливаем bash через apk
RUN apk update && apk add bash

RUN chmod +x ./entrypoint.sh

CMD ["bash", "./entrypoint.sh"]
