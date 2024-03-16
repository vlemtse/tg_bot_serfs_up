#!/bin/bash

echo "Starting update"
read -r -p "Are you sure? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    git pull origin master || { echo 'Git pull failed' ; exit 1; }
    echo "Git pull complete"

    sudo systemctl stop bot_su.service || { echo 'Stopping bot_su.service failed' ; exit 1; }
    echo "Stopping bot_su.service"

    source venv/bin/activate || { echo 'Activating venv failed' ; exit 1; }
    echo "Activating venv"

    pip install -r requirements.txt || { echo 'Installing requirements failed' ; exit 1; }
    echo "Installing requirements"

    alembic upgrade head || { echo 'Alembic upgrade failed' ; exit 1; }
    echo "Alembic upgrade completed"

    sudo systemctl start bot_su.service || { echo 'Starting bot_su.service failed' ; exit 1; }
    echo "Started bot_su.service"

    echo "Update complete"
else
    echo "Update cancelled"
fi
