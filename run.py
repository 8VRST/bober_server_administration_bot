import time

from logs.logger import telegram_bot_logger
from telegram_bot import bot, permissions
from telegram_bot.helpers import chat_id_from_message, user_id_from_message
from telegram_bot.keyboards import available_servers
from server.info_service import HardwareStat, ServerAddress
from configs.constants import SERVERS, USERS_PERMISSIONS


@bot.message_handler(commands=["start"])
def start_message(message):
    user_id = user_id_from_message(message=message)
    if str(user_id) in USERS_PERMISSIONS.keys():
        name = message.from_user.first_name
        bot.send_message(chat_id=chat_id_from_message(message=message),
                         text=f"Hi, {name}!\n\nPlease tap on your server button to get data 🦫",
                         reply_markup=available_servers.get(user_id=user_id))


@bot.message_handler(func=lambda message: message.text in SERVERS)
@permissions.only_permitted_users
def server_stat(message):
    text = ""

    hardware_stat = HardwareStat().get().items()

    for key, value in ServerAddress().get().items():
        text += f"{key}: {value}\n"

    text += "\n"

    for key, value in hardware_stat:
        text += f"{key}: {value}\n"

    chat_id = chat_id_from_message(message=message)
    user_id = user_id_from_message(message=message)

    bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown", reply_markup=available_servers.get(user_id=user_id))


@bot.message_handler(commands=["my_id"])
def my_id(message):
    bot.send_message(chat_id=chat_id_from_message(message=message), text=user_id_from_message(message=message))


@bot.message_handler()
def handler_for_everything(message):
    user_id = user_id_from_message(message=message)
    if str(user_id) in USERS_PERMISSIONS.keys():
        name = message.from_user.first_name
        bot.send_message(chat_id=chat_id_from_message(message=message),
                         text=f"Hi, {name}!\n\nPlease tap on your server button to get data 🦫",
                         reply_markup=available_servers.get(user_id=user_id))


while __name__ == "__main__":
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as error:
        telegram_bot_logger.error(error)
        time.sleep(5)
