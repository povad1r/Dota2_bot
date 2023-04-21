from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from func import get_tournament


tournament_choice = InlineKeyboardMarkup()
for tournament in get_tournament():
        button = InlineKeyboardButton(text=tournament, callback_data=tournament)
        tournament_choice.add(button)
back_button = InlineKeyboardButton(text='↩️Назад↩️', callback_data='↩️Назад↩️')
tournament_choice.add(back_button)