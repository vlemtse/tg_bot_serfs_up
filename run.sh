#!/bin/bash

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей из файла requirements.txt
pip install -r requirements.txt

# Запуск миграции alembic
alembic upgrade head

# Запуск main.py
python main.py
