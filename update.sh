#!/bin/bash


git pull origin master

sudo systemctl stop bot_su.service

pip install -r requirements.txt

alembic upgrade head

sudo systemctl start bot_su.service
