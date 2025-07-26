<h2>🚀 Установка и запуск</h2>


<h4>
1. Создайте файл .env в корневой директории согласно .env.example
</h4>

```requirements
PROJECT_NAME=
SECRET_KEY=
DEBUG=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432

REDIS_PORT=6379
```

<h4>
2. Запустите docker compose:
</h4>

```commandline
docker compose up --build -d
```
