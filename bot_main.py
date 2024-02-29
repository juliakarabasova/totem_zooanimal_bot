import asyncio

import logging
import logging.handlers

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message

from buttons_reciever import buttons_router
from trivia import router
from settings import TOKEN


dp = Dispatcher()
dp.include_router(router)
dp.include_router(buttons_router)


logger_main = logging.getLogger('totem_animal_bot')
logger_main.setLevel(logging.INFO)

handler_classes = logging.handlers.RotatingFileHandler(
    'totem_animal_bot.log',
    encoding='utf-8',
    maxBytes=500000,
    backupCount=2)
formatter_classes = logging.Formatter("%(name)s %(levelname)s [%(asctime)s] %(message)s")

handler_classes.setFormatter(formatter_classes)
logger_main.addHandler(handler_classes)


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
        'Привет! Добро пожаловать в викторину от Московского зоопарка о его обитателях *"Мое тотемное животное"*!'
        '\n\nЗдесь ты сможешь не только познакомиться с некоторыми животными, которые нашли свой дом в стенах '
        'Московского зоопарка, но и стать опекуном одного из них!'
        '\n\nУчастие в программе «Возьми животное под опеку» — это ваш личный вклад в дело сохранения биоразнообразия '
        'Земли и развитие нашего зоопарка. Подробнее о программе можно узнать по кнопке _"Подробнее об опеке"_'
        '\n\nЯ - твой гид и помощник в этом увлекательном путешествии. Готов ли ты познакомиться с миром удивительных '
        'существ и стать защитником их дома? '
        '\n\nДавай начнем прямо сейчас и узнаваем твоего тотемного животного среди жителей Московского зоопарка. '
        'Скорее жми на кнопку внизу! 🐾',
        reply_markup=keyboard,
        parse_mode='Markdown'
    )


async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
