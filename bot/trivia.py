import logging
import random

from aiogram.types import FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types

from utils import get_number_questions, get_options, get_question_text, get_winner


logging.basicConfig(filename='totem_animal_bot.log', encoding='utf-8', level=logging.INFO, filemode='a',
                    format="%(name)s %(levelname)s [%(asctime)s] %(message)s")

router = Router()
start_phrases = [
    'Поздравляю! Твое тотемное животное -',
    'Ого! Да ты же',
    'Ты бы был отличным покровителем для этого животного -',
    'Вау! Мне кажется, ты',
    'Я думаю, ты бы подружился с этим животным -',
    'Думаю, ты бы нашел общий язык с этим животным -'
]

USERS_RESULTS = {}


class TotemAnimal(StatesGroup):
    filled_questions = State()


@router.message(TotemAnimal.filled_questions)
async def iter_trivia(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        await state.update_data({f'Q{len(data)+1}': message.text.split('.')[0]})

        data = await state.get_data()

        if len(data) == get_number_questions():
            await count_result(message, state)
            await state.clear()
            return

        builder = ReplyKeyboardBuilder()

        cur_question = get_question_text(len(data) + 1)
        cur_answers = get_options(len(data) + 1)
        for date_item in cur_answers:
            builder.add(types.KeyboardButton(text=date_item))
        builder.adjust(2)

        await message.answer(
            cur_question + '\n\n' + '\n'.join(cur_answers),
            reply_markup=builder.as_markup(resize_keyboard=True),
        )

        await state.set_state(TotemAnimal.filled_questions.state)
    except:
        logging.exception(f'Exception while iter_trivia(): ')
        await message.answer(
            'Извините! В боте произошла ошибка, команда уже осведомлена об этом. Пожалуйста, повторите попытку позже.'
        )


async def count_result(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        winner = get_winner(data)

        USERS_RESULTS[message.from_user.id] = data
        USERS_RESULTS[message.from_user.id]['result'] = winner[1]

        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text='Взять животное под опеку'))
        builder.add(types.KeyboardButton(text='Попробовать еще раз'))
        builder.add(types.KeyboardButton(text='Связаться с сотрудником'))
        builder.add(types.KeyboardButton(text='Оставить отзыв о викторине'))

        builder.adjust(2)

        photo = FSInputFile(f"../images/{winner[0]}.jpg")
        await message.answer_photo(
            photo,
            caption=f"{random.choice(start_phrases)} *{winner[1]}*"
                    f"\n\n{winner[3]}"
                    f"\n\nПодробнее о своем животном можешь узнать по этой ссылке: {winner[2]}",
            reply_markup=builder.as_markup(resize_keyboard=True),
            parse_mode='Markdown'
            )
    except:
        logging.exception(f'Exception while count_result(): ')
        await message.answer(
            'Извините! В боте произошла ошибка, команда уже осведомлена об этом. Пожалуйста, повторите попытку позже.'
        )
