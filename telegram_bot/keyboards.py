from telebot import types
from configs.constants import USERS_PERMISSIONS


class CreateInlineKeyboardMarkup:

    def _create_markup(self, btns_data: dict, one_time: bool = False, resize_keyboard: bool = True,
                       row_width: int = 4) -> types.InlineKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=one_time, resize_keyboard=resize_keyboard)
        markup.row_width = row_width

        btns = []
        for btn in btns_data:
            btns.append(types.KeyboardButton(btn))

        markup.add(*btns)
        return markup


class AvailableServers(CreateInlineKeyboardMarkup):

    def get(self, user_id: int, one_time: bool = False, resize_keyboard: bool = True,
            row_width: int = 4) -> types.InlineKeyboardMarkup:
        available_servers = USERS_PERMISSIONS.get(str(user_id)).get("servers")
        if available_servers is not None:
            if "all" in available_servers:
                available_servers.remove("all")
            if available_servers:
                btns_data = {}
                for btn in available_servers:
                    btns_data[btn] = f"{btn}_reply"
                markup = self._create_markup(btns_data=btns_data, one_time=one_time, resize_keyboard=resize_keyboard,
                                             row_width=row_width)
                return markup


available_servers = AvailableServers()
