import logging
from aiogram import Bot, Dispatcher, executor, types
from func import get_content, get_tournament
from keyboards.game_choice import game_choice
from keyboards.tournament_choice import tournament_choice
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os 
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустити бота'),
            types.BotCommand('matches', 'Подивитися найближчі матчі'),
            types.BotCommand('tournament', 'Показати матчі певного турніру')
        ]
    )


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'Hello!\nThis bot keeps track of upcoming Dota 2 esports matches.\nYou can view the list of 5 upcoming matches using the /matches command.\nYou can view the list of matches of certain tournament using the /tournament command.\nFor each game, you can find out the participating teams, start time, current score and the tournament in which the match is held .')


@dp.message_handler(commands='matches')
async def amount(message: types.Message, state: FSMContext):
    await message.answer(f'How many upcoming matches do you want to see?', reply_markup = game_choice)
    await state.set_state('matches_state')

@dp.callback_query_handler(state='matches_state')
async def process_callback_limit(callback_query: types.CallbackQuery, state: FSMContext):
    limit = int(callback_query.data)  # Extract the limit from the callback_data
    content = get_content(limit)
    for match in content:
        response = (f"\n\nTournament: {match['tournament']}\nMatch time: {match['time']}\n{match['team_1']} - {match['team_2']}")
        await bot.send_message(callback_query.from_user.id, response)
    await state.finish()

@dp.message_handler(commands='tournament')
async def tournament(message: types.Message, state: FSMContext):
    await message.answer(f'Which tournament are you interested in?', reply_markup=tournament_choice)
    await state.set_state('tournament_state')

@dp.callback_query_handler(state='tournament_state')
async def tournament_pick(callback_query: types.CallbackQuery, state: FSMContext):
    content = get_content(10)
    for match in content:
        if match['tournament'] == callback_query.data:
            response = (f"\n\nTournament: {match['tournament']}\nMatch time: {match['time']}\n{match['team_1']} - {match['team_2']}")
            await bot.send_message(callback_query.from_user.id, response)
    await state.finish()
        



async def on_startup(dp):
    await set_default_commands(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
