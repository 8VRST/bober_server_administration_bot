from telebot.types import CallbackQuery, Message


def user_id_from_message(message: Message) -> int:
    return message.from_user.id


def user_id_from_call(call: CallbackQuery) -> int:
    return call.from_user.id


def chat_id_from_message(message: Message) -> int:
    return message.chat.id


def chat_id_from_call(call: CallbackQuery) -> int:
    return call.message.chat.id


def message_id_from_call(call: CallbackQuery) -> int:
    return call.message.message_id


def message_id_from_message(message: Message) -> int:
    return message.message_id
