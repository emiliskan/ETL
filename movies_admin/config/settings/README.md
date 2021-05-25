# Настройки проекта

## База данных

Запуск бд в docker:

windows:
docker run -d --rm --name postgres -p 5432:5432 -v data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=1qasde32W postgres:13

## Настройки джанго
