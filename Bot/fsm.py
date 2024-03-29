from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):  # класс машины состояний
    add_fio_st = State()
    add_email_st = State()
    update_email_st = State()
    create_ticket_st = State()
    confirm_ticket_st = State()
