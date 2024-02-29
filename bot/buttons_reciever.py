import logging

from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router, types

from utils import get_number_questions, get_options, get_question_text
from trivia import TotemAnimal, USERS_RESULTS
from settings import ADMIN_CONTACTS


logging.basicConfig(filename='totem_animal_bot.log', encoding='utf-8', level=logging.INFO, filemode='a',
                    format="%(name)s %(levelname)s [%(asctime)s] %(message)s")

buttons_router = Router()


@buttons_router.message((F.text.lower() == "начать викторину") | (F.text.lower() == "попробовать еще раз"))
async def start_trivia(message: Message, state: FSMContext):
    await message.answer(
        f'Итак, приступим к викторине "_Твое тотемное животное_"!\n\n'
        f'Тебе предстоит ответить на {get_number_questions()} вопросов. '
        f'Ответ на каждый из них приблизит тебя к тому или иному животному. '
        f'В конце ты увидишь подробную информацию о полученном результате.\n\n'
        f'Желаю хорошо провести время!',
        parse_mode='Markdown',
    )

    try:
        builder = ReplyKeyboardBuilder()

        cur_question = get_question_text(1)
        cur_answers = get_options(1)
        for date_item in cur_answers:
            builder.add(types.KeyboardButton(text=date_item))
        builder.adjust(2)

        await message.answer(
            cur_question + '\n\n' + '\n'.join(cur_answers),
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
        await state.set_state(TotemAnimal.filled_questions.state)
    except:
        logging.exception(f'Exception while start_trivia(): ')
        await message.answer(
            'Извините! В боте произошла ошибка, команда уже осведомлена об этом. Пожалуйста, повторите попытку позже.'
        )


@buttons_router.message((F.text.lower() == "подробнее об опеке") | (F.text.lower() == "взять животное под опеку"))
async def description(message: types.Message):
    await message.answer("Основная задача Московского зоопарка с самого начала его существования это — "
                         "сохранение биоразнообразия нашей планеты. Когда вы берете под опеку животное, "
                         "вы помогаете нам в этом благородном деле."
                         "\n\nОпека — это прекрасная возможность принять участие в деле сохранения редких видов, "
                         "помочь нам в реализации природоохранных программ."
                         "В программе есть 5 уровней участия в зависимости от величини пожертвования в год."
                         "\n\nСтоимость опеки рассчитывается из ежедневного рациона питания животного. "
                         "Если вы уже выбрали животное и хотите узнать стоимость опеки над ним, "
                         "вам нужно отправить свой запрос на почту, позвонить по телефонам или оставить заявку на сайте."
                         "\n\nКонтакты:"
                         "\n+7(962) 971 38 75 c 9:00 до 18:00"
                         "\nzoofriends@moscowzoo.ru"
                         "\n\nБолее подробно здесь: https://moscowzoo.ru/my-zoo/become-a-guardian/")


@buttons_router.message(F.text.lower() == "связаться с сотрудником")
async def send_contacts(message: Message, state: FSMContext):
    await message.answer(
        f'Если тебе нужна помощь по проведению или результату викторины, ты можешь написать этому сотруднику. '
        f'Он уже осведомлен о том, как прошла твоя викторина:\n\n{ADMIN_CONTACTS}',
        # reply_markup=builder.as_markup(resize_keyboard=True),
    )

    with open('problems.txt', 'a', encoding='utf-8') as f:
        f.write(f'Новый запрос от пользователя {message.from_user.id}: {USERS_RESULTS[message.from_user.id]}\n')


class FeedbackReciever(StatesGroup):
    waiting_for_feedback = State()


@buttons_router.message(F.text.lower() == "оставить отзыв о викторине")
async def initiate_feedback(message: types.Message, state: FSMContext):
    await message.answer("В одном следующем сообщении, пожалуйста, напиши отзыв об этой викторине. Мы будем рады, "
                         "если ты оставишь достаточно подробный отзыв! Его получат и прочитают сотрудники зоопарка. "
                         "Оставь контактную информацию, если хочешь, чтобы с вами связались по поводу этого отзыва:",
                         reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove())

    await state.set_state(FeedbackReciever.waiting_for_feedback.state)


@buttons_router.message(FeedbackReciever.waiting_for_feedback)
async def collect_feedback(message: types.Message, state: FSMContext):
    with open('feedbacks.txt', 'a', encoding='utf-8') as f:
        f.write(f'Новый отзыв от пользователя {message.from_user.id}: {message.text}\n\n')

    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Взять животное под опеку'))
    builder.add(types.KeyboardButton(text='Попробовать еще раз'))
    builder.add(types.KeyboardButton(text='Связаться с сотрудником'))
    builder.add(types.KeyboardButton(text='Оставить отзыв о викторине'))

    builder.adjust(2)

    await message.answer("Спасибо! Мы приняли твой отзыв и уже внимательно его читаем!",
                         reply_markup=builder.as_markup(resize_keyboard=True))


# @buttons_router.message()
# async def echo_handler(message: Message) -> None:
#     await message.answer('Извините, я вас не понял. Пожалуйста, воспользуйтесь кнопками на клавиатуре '
#                          'или еще раз напишите команду /start.')
