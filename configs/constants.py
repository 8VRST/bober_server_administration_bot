import os
import json
import logging

from dotenv import load_dotenv


load_dotenv("configs/.env")


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


WRITE_LOGS_TO_FILE = True
OUTPUT_LOGS_TO_CONSOLE = True
LOGGING_LEVEL = logging.INFO
LOGS_PATH = "logs/logs/"
LOG_FILE_SIZE = 10485760 # bytes
LOGS_BACKUPS_NUMBER = 5


with open("configs/users_permissions.json", "r") as file:
    USERS_PERMISSIONS = json.load(file)


SERVERS = USERS_PERMISSIONS["servers"]


DISK_ROOT_PATH = "/"


BYTES_IN_GB = 1000000000 # valid for Ubuntu OS
BYTES_IN_MB = 1000000 # valid for Ubuntu OS


ROUTER_ADDR = os.getenv("ROUTER_ADDR", default="192.168.1.1")
