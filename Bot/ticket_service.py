from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Bot.email_service import send_email
from Bot.fsm import FSMFillForm
from Bot.kb import confirm_ticket_kb
from DataBase.db import get_user_db, add_ticket_db

ticket_router = Router()


@ticket_router.message(StateFilter(FSMFillForm.create_ticket_st))  # Обработчик для создания запроса
async def create_ticket(msg: Message, state: FSMContext):
    message = msg.text
    tg_id, fio, email = get_user_db(msg.from_user.id)
    ticket = [f'ФИО: {fio}', f'Email: {email}', f'Сообщение: {message}']
    ticket_message = '\n'.join(ticket)
    await state.update_data(ticket=ticket_message)
    await msg.answer(text='Вы хотите отправить следующий запрос службе поддержки:\n\n' + ticket_message,
                     reply_markup=confirm_ticket_kb)
    await state.set_state(FSMFillForm.confirm_ticket_st)


@ticket_router.callback_query(StateFilter(FSMFillForm.confirm_ticket_st))  # Обработчик для подтверждения запроса
async def process_confirm_kb(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'no':
        await callback_query.message.answer(
            text="Опишите вашу проблему и бот отправит ее на рассмотрение в службу поддержки ⬇️")
        await callback_query.message.delete()
        await state.set_state(FSMFillForm.create_ticket_st)
    else:
        data = await state.get_data()
        print(data['ticket'])
        send_email(data['ticket'])
        add_ticket_db(callback_query.from_user.id, data['ticket'])
        await callback_query.message.edit_text(
            text="Вы отправили службе поддержки следующий запрос:\n\n" + data['ticket'])
        await callback_query.answer(text="Ваше сообщение отправлено службе поддержки ✅", show_alert=True)
        await state.clear()
