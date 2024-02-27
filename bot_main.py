import aiohttp
import asyncio

import logging
import logging.handlers
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from trivia import router, TotemAnimal
from utils import get_number_questions, get_options, get_question_text


dp = Dispatcher()
dp.include_router(router)

TOKEN = '7009627612:AAEyufBbd7Jgt5jCts7d6FAzW8T1cyyCiY4'


"""
Criteria:

1. Запуск бота
2. Взаимодействие с пользователем
3. Модуль викторины
4. Алгоритм обработки ответов
5. Подведение результатов
6. Работа с изображениями
7. Поддержка социальных сетей
8. Контактный механизм
9. Возможность перезапуска
10. Механизм обратной связи
11. Конфиденциальность и безопасность данных
12. Масштабируемость                            # тянуть вопросы из столбцов бд? а варианты - set из значений колонны
13. Мониторинг производительности               # просто logging?
14. Сопровождение пользователя
15. Креативность и уникальность
"""


def initiate_logging():
    logger_classes = logging.getLogger('totem_animal_bot')
    logger_classes.setLevel(logging.INFO)

    handler_classes = logging.handlers.RotatingFileHandler(
        'totem_animal_bot.log',
        encoding='utf-8',
        maxBytes=500000,
        backupCount=2)
    formatter_classes = logging.Formatter("%(name)s %(levelname)s [%(asctime)s] %(message)s")

    handler_classes.setFormatter(formatter_classes)
    logger_classes.addHandler(handler_classes)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    kb = [
        [
            types.KeyboardButton(text="Начать викторину"),
            types.KeyboardButton(text="Подробнее об опеке"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(
        f"Привет! Я бот продвигающий программу опеки от Московского зоопарка. "
        f"Ты можешь почитать об опеке или сразу начать викторину, которая покажет, какое животное тебе близко по духу"
        f"и расскажет как ты сможешь ему помочь в нашем зоопарке! :)",
        reply_markup=keyboard
    )


@dp.message(F.text.lower() == "начать викторину" or F.text.lower() == "начать заново")
async def start_trivia(message: Message, state: FSMContext):
    await message.answer(
        f"Добро пожаловать в викторину '_Твое тотемное животное_'!\n\n"
        f"Тебе предстоит ответить на {get_number_questions()} вопросов. "        # TODO: может задать дб здесь и передавать ее?
        f"Ответ на каждый из них приблизит тебя к тому или иному животному."
        f"В конце ты увидишь подробную информацию о полученном результате.\n\n"
        f"Желаю хорошо провести время!",
        parse_mode='Markdown',
    )

    builder = ReplyKeyboardBuilder()

    cur_question = get_question_text(1)
    cur_answers = get_options(1)
    for date_item in cur_answers:
        builder.add(types.KeyboardButton(text=date_item))
    builder.adjust(2)

    await message.answer(
        cur_question,
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(TotemAnimal.filled_questions.state)


@dp.message(F.text.lower() == "подробнее об опеке")
async def description(message: types.Message):
    await message.answer("Тут будет инфа и ссылка на программу опеки из курса скиллфактори.")


async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    initiate_logging()
    asyncio.run(main())
