from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from Bot.config import LMS_URL

web_app_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="SPBGUT LMS", web_app=WebAppInfo(url=LMS_URL))]],
    resize_keyboard=True)

contact_kb1 = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Связаться со службой поддержки 📞")]],
    resize_keyboard=True, one_time_keyboard=True)

confirm_ticket_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="✅", callback_data='yes'),
                      InlineKeyboardButton(text="❌", callback_data='no')]],
    resize_keyboard=True)
