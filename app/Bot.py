import requests
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from BotConfig import API_TOKEN
import app.AlertsBase.bdrequests as rq
from app.AlertsBase.bdrequests import messageAlerts, get_alerts
async def rasilka():
    while 1:
        await messageAlerts()

router = Router()



class Crypto(StatesGroup):
    val1 = State()
    val2 = State()
class Alert(StatesGroup):
    val1 = State()
    val2 = State()
    costProcent = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply('Вас приветствует Erat бот! Я могу узнать курс криптовалют или установить alert. Что вам нужно сегодня?', reply_markup=kb.mai)
@router.message(Command('ok'))
async def get_help(message: Message):
    await message.answer('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

@router.message(F.text == "Крипта")
async def how_are_you(message: Message):
    await  rasilka()

@router.message(F.text == 'Узнать курс валюты')
async def reg_one(message: Message,state: FSMContext):
    await state.set_state(Crypto.val1)
    await message.answer('Введите название валюты')

@router.message(F.text == 'Узнать свои Alerts')
async def reg_one(message: Message):
    await get_alerts(message.from_user.id)

@router.message(Crypto.val1)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(val1 = message.text)
    await state.set_state(Crypto.val2)
    await message.answer('Введите название валюты, в которой отобразится курс')
@router.message(Crypto.val2)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(val2 = message.text)
    data = await state.get_data()
    CRresponse = requests.get(
        f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={data["val1"]}&tsyms={data["val2"]}&api_key={API_TOKEN}")
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
    await state.update_data(val1=message.text)
    await state.set_state(Alert.val2)
    await message.answer('Введите название валюты, в которой будет использоваться курс')

@router.message(Alert.val2)
async def alert_three(message: Message, state: FSMContext):
    await state.update_data(val2=message.text)
    await state.set_state(Alert.costProcent)
    await message.answer('Введите процент')

@router.message(Alert.costProcent)
async def alert_four(message: Message, state: FSMContext):
    await state.update_data(costProcent=message.text)
    data = await state.get_data()
    CRresponse = requests.get(
    f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={data["val1"]}&tsyms={data["val2"]}&api_key={API_TOKEN}")
    if "Response" in CRresponse.json():
        await message.answer("Что-то пошло не так, введите заново")
    else:
        cost = str(CRresponse.json()[data["val1"]][data["val2"]])
        data["costProcent"] = str(float(cost) * (float(data["costProcent"]) / 100))
        await rq.setAlert(message.from_user.id,cost,data["costProcent"],data["val1"],data["val2"])
        await message.answer("Alert успешно установлен!")
        await state.clear()


