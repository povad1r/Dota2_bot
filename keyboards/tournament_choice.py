from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from func import get_tournament


tournament_choice = InlineKeyboardMarkup()
for tournament in get_tournament():
        button = InlineKeyboardButton(text=tournament, callback_data=tournament)
        tournament_choice.add(button)