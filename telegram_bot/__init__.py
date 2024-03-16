from telebot import TeleBot, apihelper

from configs.constants import TELEGRAM_BOT_TOKEN


apihelper.SESSION_TIME_TO_LIVE = 5 * 60


bot = TeleBot(TELEGRAM_BOT_TOKEN)
