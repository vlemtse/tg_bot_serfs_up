#!/bin/bash

echo "Starting update"
git pull origin master
echo "Git pull complete"

sudo systemctl stop bot_su.service
echo "Stopping bot_su.service"

source venv/bin/activate && pip install -r requirements.txt
echo "Activating venv and installing requirements"

alembic upgrade head
echo "Alembic upgrade completed"

sudo systemctl start bot_su.service
echo "Started bot_su.service"

echo "Update complete"
