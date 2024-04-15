from app.AlertsBase.models import async_session
from app.AlertsBase.models import User,Alert
from sqlalchemy import select, delete
from BotConfig import API_TOKEN, TOKEN
from aiogram import Bot
import requests
import math

bot = Bot(token=TOKEN)
async def set_user(tg_id) :
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()

async def get_alerts(tg_id) :
    async with async_session() as session:
        fl = 1
        alerts = await session.scalars(select(Alert).where(Alert.user_id == tg_id))

        for alert in alerts:
            await bot.send_message(chat_id=tg_id, text=f"{alert.val1} c разницей {alert.procent} {alert.val2}")
            fl = 0
        if fl == 1:
            await bot.send_message(chat_id=tg_id, text="У вас нет Alerts")


async def setAlert(user_id,cost,procent,val1,val2):
    async with async_session() as session:
        session.add(Alert(user_id = user_id,cost = cost, procent = procent,val1 = val1, val2 = val2))
        await session.commit()

async def messageAlerts():
    async with async_session() as session:
        await session.scalars(select(Alert))
        async with async_session() as session:
            Alerts = await session.scalars(select(Alert))
            for AlertObject in Alerts:
                New_rq = requests.get(
                    f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={AlertObject.val1}&tsyms={AlertObject.val2}&api_key={API_TOKEN}")
                cost = float(New_rq.json()[AlertObject.val1][AlertObject.val2])
                #rasnitsa = abs(float(AlertObject.cost) - cost)
                if 99999 > float(AlertObject.procent): #rasnitsa
                    await  session.execute(delete(Alert).where(Alert.id == AlertObject.id))
                    if float(AlertObject.cost) > cost:
                        await bot.send_message(chat_id=AlertObject.user_id,text=f"ALERT! Цена {AlertObject.val1}  упала на  {AlertObject.procent} {AlertObject.val2} ")
                    else:
                        await bot.send_message(chat_id=AlertObject.user_id,text=f"ALERT! Цена {AlertObject.val1}  возросла на {AlertObject.procent} {AlertObject.val2}")
            await session.commit()



