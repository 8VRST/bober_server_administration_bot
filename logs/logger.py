import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from configs.constants import LOGS_PATH, LOGGING_LEVEL, LOG_FILE_SIZE, LOGS_BACKUPS_NUMBER, WRITE_LOGS_TO_FILE, \
    OUTPUT_LOGS_TO_CONSOLE


class SetupLogger:

    def __init__(self, module_name: str, logging_level: int = LOGGING_LEVEL, logs_path: str = LOGS_PATH,
                 log_file_size: int = LOG_FILE_SIZE, backups_number: int = LOGS_BACKUPS_NUMBER):

        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging_level)
        log_file = f"{logs_path if '/' in logs_path else logs_path + '/'}{module_name}.log"
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        self.file_handler = RotatingFileHandler(log_file, maxBytes=log_file_size, backupCount=backups_number)
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setLevel(logging.INFO)
        self.stream_handler.setFormatter(self.formatter)

    def get_logger(self, file: bool = WRITE_LOGS_TO_FILE, console: bool = OUTPUT_LOGS_TO_CONSOLE):
        if file:
            self.logger.addHandler(self.file_handler)
        if console:
            self.logger.addHandler(self.stream_handler)
        return self.logger


__setup_telegram_bot_logger = SetupLogger(module_name="TELEGRAM BOT LOGGER")
telegram_bot_logger = __setup_telegram_bot_logger.get_logger()


__setup_server_logger = SetupLogger(module_name="SERVER LOGGER")
server_logger = __setup_server_logger.get_logger()
