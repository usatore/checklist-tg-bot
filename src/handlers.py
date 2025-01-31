from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from src.lexicon import LEXICON, ALL_QUESTS
from src.storage import global_quests, users_db, users_nicknames
from copy import deepcopy
from aiogram.types import Message, CallbackQuery
from src.keyboards import create_quests_keyboard
from src.config import ADMIN_ID
import os
KEK = os.getenv('KEK')

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start'])
    if message.from_user.id not in users_db:
        users_nicknames[message.from_user.id] = message.from_user.username
        users_db[message.from_user.id] = deepcopy(global_quests)


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])

@router.message(Command(commands='status'))
async def process_status_command(message: Message):
    user_quests = users_db[message.from_user.id]
    await message.answer(
        text='Ваши статусы выполнения квестов:',
        reply_markup=create_quests_keyboard(
            *[quest_name + ' ' + quest_status for quest_name, quest_status in user_quests.items()]
        )
    )

@router.message(Command(commands='quests'))
async def process_quests_command(message: Message):
    await message.answer(
        text='Задания к квестам:',
        reply_markup=create_quests_keyboard(
            *[quest_name for quest_name in ALL_QUESTS]
        )
    )


@router.message(Command(commands='admin'))
async def process_quests_command(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            text='You are admin',
            reply_markup=create_quests_keyboard(
                'check results',
            )
        )
    else:
        await message.answer(
            text='You are not admin'
        )

@router.callback_query(F.data == 'check results')
async def process_check_results_callback(callback_query: CallbackQuery):
    for user_id in users_db:
        await callback_query.message.answer(text=f'{KEK}{users_nicknames[user_id]}\n{users_db[user_id]}')
        print(KEK)

@router.callback_query(F.data.endswith('❌'))
async def process_status_no_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_quests = users_db[user_id]
    users_db[user_id][callback_query.data[:-2]] = '✅'
    await callback_query.message.edit_reply_markup(
        reply_markup=create_quests_keyboard(
            *[quest_name + ' ' + quest_status for quest_name, quest_status in user_quests.items()]
        )
    )

@router.callback_query(F.data.endswith('✅'))
async def process_status_yes_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_quests = users_db[user_id]
    users_db[user_id][callback_query.data[:-2]] = '❌'
    await callback_query.message.edit_reply_markup(
        reply_markup=create_quests_keyboard(
            *[quest_name + ' ' + quest_status for quest_name, quest_status in user_quests.items()]
        )
    )



@router.callback_query(F.data)
async def process_quest_callback(callback_query: CallbackQuery):
    # Получаем данные из callback_data, например: quest_1
    quest_data = callback_query.data
    print(quest_data)
    # Для примера, обрабатываем quest_data и выводим сообщение
    await callback_query.answer(f"Вы выбрали квест: {quest_data}")
    # Отправляем сообщение о выбранном квесте или выполняем нужные действия
    await callback_query.message.answer(ALL_QUESTS[quest_data])
