import smtplib
from email.mime.text import MIMEText

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from validate_email import validate_email
import DNS

from Bot.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIEVER
from Bot.fsm import FSMFillForm
from DataBase.db import add_user_db, update_email_db, get_user_db

DNS.defaults['server'] = ['8.8.8.8', '8.8.4.4']  # использование dns-серверов Google

email_router = Router()


@email_router.message(StateFilter(FSMFillForm.add_email_st))
async def add_email(msg: Message, state: FSMContext):
    email = msg.text
    if validate_email(email, verify=True):  # Проверка валидности email
        data = await state.get_data()
        add_user_db(msg.from_user.id, data['fio'], email)  # Добавление пользователя в базу данных
        await msg.answer(text="Email принят ✅")
        await msg.answer(text="Опишите вашу проблему и бот отправит ее на рассмотрение в службу поддержки ⬇️")
        await state.set_state(FSMFillForm.create_ticket_st)
    else:
        await msg.answer(text="Такого email не существует, попробуйте ввести email заново ♻️")
        await state.set_state(FSMFillForm.add_email_st)  # Повторный запрос на ввод email


@email_router.message(Command(commands='change_email'))  # Обработчик для команды изменения email
async def transfer_to_add_email(msg: Message, state: FSMContext):
    if get_user_db(msg.from_user.id) is None:
        await msg.answer(text="Функция доступна только зарегистрированным пользователям ⚠️")
        return
    await msg.answer(text="Введите ваше email ⬇️")
    await state.set_state(FSMFillForm.update_email_st)


@email_router.message(StateFilter(FSMFillForm.update_email_st))
async def update_email(msg: Message, state: FSMContext):
    email = msg.text
    if validate_email(email, verify=True):  # Проверка валидности email
        update_email_db(msg.from_user.id, email)
        await msg.answer(text="Email обновлён ✅")
        await state.clear()
    else:
        await msg.answer(
            text="Такого email не существует, попробуйте ввести email заново ❌")
        await state.set_state(FSMFillForm.update_email_st)  # Повторный запрос на ввод email


def send_email(text):
    sender = EMAIL_SENDER
    password = EMAIL_PASSWORD
    reciever = EMAIL_RECIEVER
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(sender, password)
        msg = MIMEText(text)
        msg["Subject"] = "LMS Help"
        server.sendmail(sender, reciever, msg.as_string())
        print("The message was sent successfully!")
    except Exception as _ex:
        print(f"{_ex}\nThe message was not sent")
