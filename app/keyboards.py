from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup,InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder

mai = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Узнать курс валюты')],
    [KeyboardButton(text='Установить alert'),KeyboardButton(text='Чистка'),KeyboardButton(text='Начать отслеживание'),KeyboardButton(text='Узнать свои Alerts')]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт'
)

 ##directi = InlineKeyboardButton(inline_keyboard=[
  ##  [InlineKeyboardButton(text = 'Вверх',callback_data = 'Вверх')],
  ##  [InlineKeyboardButton(text = 'Вниз',callback_data = 'Вниз')]])
