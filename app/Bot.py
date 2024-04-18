import asyncio
import os
import threading
import requests
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
import app.AlertsBase.bdrequests as rq
from app.AlertsBase.bdrequests import messageAlerts, get_alerts, delete_my_alerts
from dotenv import load_dotenv
load_dotenv()
def rasilka():
    while 1:
        asyncio.run(messageAlerts())
threading.Thread(target=rasilka).start()
router = Router()
def is_float(string):
  try:
    return float(string) and '.' in string  # True if string is a number contains a dot
  except ValueError:  # String is not a number
    return False

class Crypto(StatesGroup):
    val1 = State()
    val2 = State()
class Alert(StatesGroup):
    val1 = State()
    val2 = State()
    costProcent = State()
    direction = State()
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply('Вас приветствует Erat бот! Я могу узнать курс криптовалют или установить alert. Что вам нужно сегодня?', reply_markup=kb.mai)
@router.message(F.text == 'Чистка')
async def chistka(message: Message):
    await delete_my_alerts(message.from_user.id)
    await message.answer('Alerts удалены ')
@router.message(F.text == 'Проверить Alerts')
async def proverka(message: Message):
    await get_alerts(message.from_user.id)
@router.message(F.text == 'Курс валюты')
async def kurs_one(message: Message,state: FSMContext):
    await state.set_state(Crypto.val1)
    await message.answer('Введите название валюты')

@router.message(Crypto.val1)
async def kurs_two(message: Message, state: FSMContext):
    await state.update_data(val1 = (message.text).upper())
    await state.set_state(Crypto.val2)
    await message.answer('Введите название валюты, в которой отобразится курс')
@router.message(Crypto.val2)
async def kurs_three(message: Message, state: FSMContext):
    await state.update_data(val2 = (message.text).upper())
    data = await state.get_data()
    CRresponse = requests.get(
        f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={data["val1"]}&tsyms={data["val2"]}&api_key={os.getenv('API_TOKEN')}")
    if "Response" in CRresponse.json():
        await message.answer("Что-то пошло не так, введите заново")
    else:
        await message.answer("".join([f"1 {data["val1"]} = ",str(CRresponse.json()[data["val1"]][data["val2"]]),f" {data["val2"]}"]))
    await state.clear()

@router.message(F.text == 'Установить alert')
async def alert_one(message: Message, state: FSMContext):
    await state.set_state(Alert.val1)
    await message.answer('Введите название валюты, для которой хотите установить alert')

@router.message(Alert.val1)
async def alert_two(message: Message, state: FSMContext):
    await state.update_data(val1=(message.text).upper())
    await state.set_state(Alert.val2)
    await message.answer('Введите название валюты, в которой будет использоваться курс')

@router.message(Alert.val2)
async def alert_three(message: Message, state: FSMContext):
    await state.update_data(val2=(message.text).upper())
    await state.set_state(Alert.costProcent)
    await message.answer('Введите процент')

@router.message(Alert.costProcent)
async def alert_four(message: Message, state: FSMContext):
    await state.update_data(costProcent=message.text)
    await state.set_state(Alert.direction)
    await message.answer('Выберите направление курса',reply_markup=kb.lowup)

@router.message(Alert.direction)
async def alert_five(message: Message, state: FSMContext):
    await state.update_data(direction=(message.text).lower())
    data = await state.get_data()
    CRresponse = requests.get(
    f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={data["val1"]}&tsyms={data["val2"]}&api_key={os.getenv('API_TOKEN')}")
    if ("Response" in CRresponse.json() or (not(data["costProcent"].isdigit()) and not(is_float(data["costProcent"]))) or (data['direction']
            != 'вверх' and data['direction'] != 'вниз')):
        await message.answer("Что-то пошло не так, введите заново",reply_markup=kb.mai)
    else:
        cost = str(CRresponse.json()[data["val1"]][data["val2"]])
        data["costProcent"] = str(float(cost) * (float(data["costProcent"]) / 100))
        await rq.setAlert(message.from_user.id,cost,data["costProcent"],data["val1"],data["val2"],data["direction"])
        await message.answer(f"Alert в точке {cost} для {data['val1']} в {data['val2']} с направлением {data['direction']} успешно установлен!",reply_markup=kb.mai)
        await state.clear()



