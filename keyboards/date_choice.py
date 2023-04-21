from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from func import get_date


date_choice = InlineKeyboardMarkup()
for date in get_date():
        button = InlineKeyboardButton(text=date, callback_data=date)
        date_choice.add(button)
back_button = InlineKeyboardButton(text='↩️Назад↩️', callback_data='↩️Назад↩️')
date_choice.add(back_button)