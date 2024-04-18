from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder

mai = ReplyKeyboardMarkup(keyboard=[

    [KeyboardButton(text='Установить alert'),KeyboardButton(text='Проверить Alerts')],
    [KeyboardButton(text='Курс валюты'),KeyboardButton(text='Чистка')]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт'
)

lowup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Вверх'),KeyboardButton(text='Вниз')]],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт'
)

