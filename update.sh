#!/bin/bash

echo "Starting update"
git pull origin master
echo "Git pull complete"

sudo systemctl stop bot_su.service
echo "Stopping bot_su.service"

pip install -r requirements.txt
echo "Requirements installed"

alembic upgrade head
echo "Alembic upgrade completed"

sudo systemctl start bot_su.service
echo "Started bot_su.service"

echo "Update complete"
