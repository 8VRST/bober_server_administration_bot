import functools

from logs.logger import telegram_bot_logger
from configs.constants import USERS_PERMISSIONS


def only_permitted_users(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        user_id = str(args[0].from_user.id)
        user_msg = args[0].text
        username = args[0].chat.first_name

        condition1 = user_id in USERS_PERMISSIONS.keys() and user_msg in USERS_PERMISSIONS.get(user_id, {}).get("servers")
        condition2 = user_id in USERS_PERMISSIONS.keys() and "all" in USERS_PERMISSIONS.get(user_id, {}).get("servers")

        permitted = condition1 or condition2

        if permitted:
            return func(*args, **kwargs)
        telegram_bot_logger.warning(f"To execute this action user {username} {user_id} should be in permitted group")
    return wrapper
