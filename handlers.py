import logging
from aiogram import Bot, Dispatcher, executor, types
from func import get_content
from keyboards.game_choice import game_choice
from keyboards.tournament_choice import tournament_choice
from keyboards.date_choice import date_choice
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
            types.BotCommand('tournament', 'Показати матчі певного турніру'),
            types.BotCommand('date', 'Показати матчі на певну дату'),
            types.BotCommand('support', 'Звернутися до служби підтримки')
        ]
    )


@dp.callback_query_handler(text='↩️Назад↩️', state='*')
async def go_back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state('default')
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, f'Ти знову можеш використовувати команди!')


@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
    await message.answer(f'Привіт! Цей бот відстежує майбутні кіберспортивні матчі по Dota 2🕹️.\n⚪ Ви можете переглянути список майбутніх матчів за допомогою команди /matches.\n⚪ Ви можете переглянути список матчів певного турніру🏆 за допомогою команди /tournament.\n⚪ Ви можете переглянути список матчів на певну дату📅 за допомогою команди /date.\n⚪ Ви можете звернутися до підтримки за допомогою команди /support\n⚪ Для кожної гри ви можете дізнатися команди-учасниці, час початку, поточний рахунок і турнір, в якому проводиться матч.')
    await state.set_state('default')


@dp.message_handler(commands='matches', state='default')
async def amount(message: types.Message, state: FSMContext):
    await message.answer(f'Скільки матчів ви хочете побачити?', reply_markup = game_choice)
    await state.set_state('matches_state')


@dp.callback_query_handler(state='matches_state')
async def process_callback_limit(callback_query: types.CallbackQuery):
    limit = int(callback_query.data)
    content = get_content(limit)
    for match in content:
        response = (f"\n\n▪️ Tournament: {match['tournament']}▪️\n▪️ Match time: {match['time']}▪️\n▫️{match['team_1']}{match['score']} {match['team_2']}▫️")
        await bot.send_message(callback_query.from_user.id, response)


@dp.message_handler(commands='tournament', state='default')
async def tournament(message: types.Message, state: FSMContext):
    await message.answer(f'Який саме турнір вас цікавить🏆?', reply_markup=tournament_choice)
    await state.set_state('tournament_state')


@dp.callback_query_handler(state='tournament_state')
async def tournament_pick(callback_query: types.CallbackQuery):
    content = get_content(50)
    for match in content:
        if match['tournament'] == callback_query.data:
            response = (f"\n\n▪️ Tournament: {match['tournament']}▪️\n▪️ Match time: {match['time']}▪️\n▫️ {match['team_1']} {match['score']} {match['team_2']}▫️")
            await bot.send_message(callback_query.from_user.id, response)


@dp.message_handler(commands='date', state='default')
async def date(message: types.Message, state: FSMContext):
    await message.answer(f'Яка дата вас цікавить📅?', reply_markup=date_choice)
    await state.set_state('date_state')


@dp.callback_query_handler(state='date_state')
async def date_pick(callback_query: types.CallbackQuery):
    content = get_content(50)
    for match in content:
        if match['date'] == callback_query.data:
            response = (f"\n\n▪️ Tournament: {match['tournament']}▪️\n▪️ Match time: {match['time']}▪️\n▫️ {match['team_1']} {match['score']} {match['team_2']}▫️")
            await bot.send_message(callback_query.from_user.id, response)

@dp.message_handler(commands='support', state='default')
async def support(message: types.Message, state: FSMContext):
    await message.answer('Для вирішення проблеми пишіть @povad1r')
    await state.set_state('default')

async def on_startup(dp):
    await set_default_commands(dp)



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
