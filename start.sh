#!/bin/bash

# Sequence of commands to activate backend
if [ ! -f .env.example ]; then
    echo "[X] - ERROR: .env.example file does not exist!"
    exit 1
fi

cp .env.example .env

echo [*] - Syncing dependencies
uv sync &> /dev/null
echo [V] -- DONE

echo [*] - Building db
{
    docker-compose up -d

    source .venv/bin/activate

    sleep 2 # wait for db

    alembic upgrade head
} &> /dev/null
echo [V] -- DONE

echo [*] - Populating db
python3 app/alembic/seeders/default_seeder.py &> /dev/null
echo [V] -- DONE

echo [*] - Starting fastapi
fastapi run --reload
