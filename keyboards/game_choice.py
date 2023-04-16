from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

game_choice = InlineKeyboardMarkup()
limit = 0
for a in range(5):
        limit +=3
        button = InlineKeyboardButton(text=limit, callback_data=limit)
        game_choice.add(button)
