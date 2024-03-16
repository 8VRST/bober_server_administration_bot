# OS Ubuntu 22.x.x, Python 3.11.x 

1. Create virtual environment: `python3.11 -m venv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r deploy/requirements.txt`
4. Set valid telegram bot token in `deploy/.env.example` file and rename file to `deploy/.env`
5. Setup telegram users (name: telegram_id) in `deploy/users_permissions.example.json` and rename file to `deploy/users_permissions.json`
6. Run bot with command: `python run.py`

**Deploy:**
1. Check configurations in `deploy/bober-server-administration-bot.example.service` file and rename file to `deploy/bober-server-administration-bot.service`
2. Copy service file into the systemd directory: `sudo cp deploy/bober-server-administration-bot.service /etc/systemd/system/`
3. Reload systemctl daemon: `sudo systemctl daemon-reload`
4. Start service: `sudo systemctl start bober-server-administration-bot.service`
5. Autostart on system startup: `sudo systemctl enable bober-server-administration-bot.service`
