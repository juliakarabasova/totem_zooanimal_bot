import aiohttp
import asyncio

import logging
import logging.handlers
import sys
import random

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types

from utils import get_number_questions, get_options, get_question_text, get_winner


router = Router()
start_phrases = [
    'Поздравляю! Твое тотемное животное -',
    'Ого! Да ты же',
    'Ты бы был отличным покровителем для этого животного -',
    'Вау! Мне кажется, ты',
    'Я думаю, ты бы подружился с этим животным -',
    'Думаю, ты бы нашел общий язык с этим животным -'
]


class TotemAnimal(StatesGroup):
    filled_questions = State()


@router.message(TotemAnimal.filled_questions)
async def iter_trivia(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({f'Q{len(data)+1}': message.text.split('.')[0]})

    data = await state.get_data()
    print(data)
    if len(data) == get_number_questions():             # Итерации попадают в эту функцию до тех пор, пока не дойдут до последнего вопроса
        await count_result(message, state)
        return

    builder = ReplyKeyboardBuilder()

    cur_question = get_question_text(len(data) + 1)
    cur_answers = get_options(len(data) + 1)
    for date_item in cur_answers:
        builder.add(types.KeyboardButton(text=date_item))
    builder.adjust(2)

    await message.answer(
        cur_question,
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

    await state.set_state(TotemAnimal.filled_questions.state)


async def count_result(message: types.Message, state: FSMContext):
    data = await state.get_data()
    winner = get_winner(data)

    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Взять животное под опеку'))
    builder.add(types.KeyboardButton(text='Начать заново'))

    # photo = open('images/1.jpg', 'rb')
    photo = FSInputFile(f"images/{winner[0]}.jpg")
    await message.answer_photo(
        photo,
        caption=f"{random.choice(start_phrases)} *{winner[1]}*"
                f"\n\n{winner[3]}"
                f"\n\nПодробнее о своем животном можешь узнать по этой ссылке: {winner[2]}",
        reply_markup=builder.as_markup(resize_keyboard=True),
        parse_mode='Markdown'
        )

    # await message.answer(
    #     f"Поздравляю, твое тотемное животное - *{winner[0]}*"
    #     f"\n\n{winner[1]}",
    #     reply_markup=builder.as_markup(resize_keyboard=True),
    #     parse_mode='Markdown'
    # )
