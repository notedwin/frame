#!/bin/bash
set -e

# set a variable for host
host="notedwin@192.168.0.134"

ansible-playbook -i "${host}", deploy.yml
scp .env "${host}":~/src/.env
scp frame.py "${host}":~/src/frame.py

scp pyproject.toml "${host}":~/src/pyproject.toml

# crontab - create a new crontab
ssh "${host}" "echo '@reboot /usr/bin/tmux new-session -d -s notedwin \"cd /home/notedwin/src && uv run frame.py\"' | crontab -"

# on the pi, install the following packages
# uv pip install gpiozero pi-heif pillow python-dotenv requests schedule inky
# uv pip install pi-heif --index-url https://pypi.org/simple

# for now manually run using:
# /usr/bin/tmux new-session -d -s notedwin 'cd /home/notedwin/src && uv run frame.py'