#!/bin/bash
set -e

# set a variable for host
host="notedwin@192.168.0.134"

ansible-playbook -i "${host}", deploy.yml
scp .env "${host}":~/src/.env
scp frame.py "${host}":~/src/frame.py

scp pyproject.toml "${host}":~/src/pyproject.toml


# curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR="/usr/bin" sh
ssh "${host}" "echo '@reboot /usr/bin/uv run --project /home/notedwin/src /home/notedwin/src/frame.py >> /home/notedwin/log 2>&1' | crontab -"

# on the pi, install the following packages
# uv pip install gpiozero pi-heif pillow python-dotenv requests schedule inky
# uv pip install pi-heif --index-url https://pypi.org/simple