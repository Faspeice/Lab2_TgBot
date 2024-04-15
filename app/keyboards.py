from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder

mai = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Узнать курс валюты')],
    [KeyboardButton(text='Установить alert'),KeyboardButton(text='BTC'),KeyboardButton(text='ETH'),KeyboardButton(text='Узнать свои Alerts')]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт'
)
