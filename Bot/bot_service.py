from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter, Command
from kb import web_app_kb, contact_kb1
from DataBase.db import get_user_db
from aiogram.fsm.context import FSMContext  # Импорт контекста машины состояний из библиотеки aiogram
from fsm import FSMFillForm  # Импорт класса машины состояний из файла fsm

main_router = Router()  # Создание роутера для обработчиков сообщений


@main_router.message(CommandStart())  # Обработчик для команды /start
async def start(msg: Message, state: FSMContext):
    # Отправка стикера и кнопки связи со службой поддержки
    await state.clear()
    await msg.delete()
    await msg.answer_sticker(sticker=r"CAACAgIAAxkBAAELvptl-U7VQ4-2_nnELP1pIiozZeshvgACCAEAAmpMyiQcAURrhkDLDDQE",
                             reply_markup=contact_kb1)
    await lms(msg)


@main_router.message(Command(commands='lms'))  # Обработчик для команды '/lms'
async def lms(msg: Message):
    # Отправка сообщения и inline-кнопки с web app
    await msg.answer(text="Welcome to <b>SUT LMS BOT</b>",
                     reply_markup=web_app_kb)


@main_router.message(F.text == "Связаться со службой поддержки 📞")  # Обработчик для кнопки связи с поддержкой
async def contact_support(msg: Message, state: FSMContext):
    # Проверка зарегистрирован ли пользователь и установка соответствующего состояния
    if get_user_db(tg_id=msg.from_user.id):
        await msg.answer(text="Опишите вашу проблему и бот отправит ее на рассмотрение в службу поддержки ⬇️")
        await state.set_state(FSMFillForm.create_ticket_st)
    else:
        await msg.answer(text="Для связи со службой поддержки необходимо зарегистрироваться ⚠️")
        await msg.answer(text="Введите ваше ФИО ⬇️")
        await state.set_state(FSMFillForm.add_fio_st)


@main_router.message(StateFilter(FSMFillForm.add_fio_st))  # Обработчик для добавления ФИО
async def add_fio(msg: Message, state: FSMContext):
    fio = msg.text
    await state.update_data(fio=fio)  # Обновление данных в состоянии
    await msg.answer(text="Введите ваше email ⬇️")
    await state.set_state(FSMFillForm.add_email_st)
