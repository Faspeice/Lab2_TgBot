import asyncio
import os

from app.AlertsBase.models import async_session
from app.AlertsBase.models import User,Alert
from sqlalchemy import select, delete
from aiogram import Bot
import requests
from dotenv import load_dotenv
load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
async def set_user(tg_id) :
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()
            await asyncio.sleep(1)

async def get_alerts(tg_id) :
    async with async_session() as session:
        fl = 1
        alerts = await session.scalars(select(Alert).where(Alert.user_id == tg_id))

        for alert in alerts:
            await bot.send_message(chat_id=tg_id, text=f"{alert.val1} с точки {alert.cost}, направлением {alert.direction}  и разницей {alert.procent} {alert.val2}")
            fl = 0
        if fl == 1:
            await bot.send_message(chat_id=tg_id, text="У вас нет Alerts")


async def setAlert(user_id,cost,procent,val1,val2,direction):
    async with async_session() as session:
        session.add(Alert(user_id = user_id,cost = cost, procent = procent,val1 = val1, val2 = val2,direction = direction))
        await session.commit()
        await asyncio.sleep(1)

async def delete_my_alerts(user_id):
    async with async_session() as session:
        await session.scalars(select(Alert))
        async with async_session() as session:
            await session.execute(delete(Alert).where(Alert.user_id == user_id))
            await session.commit()
            await asyncio.sleep(1)


async def messageAlerts():
    async with async_session() as session:
        await session.scalars(select(Alert))
        async with async_session() as session:
            Alerts = await session.scalars(select(Alert))
            for AlertObject in Alerts:
                New_rq = requests.get(
                    f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={AlertObject.val1}&tsyms={AlertObject.val2}&api_key={os.getenv('API_TOKEN')}")
                cost = float(New_rq.json()[AlertObject.val1][AlertObject.val2])
                if New_rq:
                    if AlertObject.direction == "вверх":
                        rasnitsa = ( cost - float(AlertObject.cost))
                    elif AlertObject.direction == "вниз":
                        rasnitsa = (float(AlertObject.cost) - cost)
                    if rasnitsa > float(AlertObject.procent): #rasnitsa
                        await  session.execute(delete(Alert).where(Alert.id == AlertObject.id))
                        if AlertObject.direction == "вверх":
                            await bot.send_message(chat_id=AlertObject.user_id,text=f"ALERT: Цена {AlertObject.val1} c точки {AlertObject.cost} возросла на {rasnitsa} {AlertObject.val2}")
                        elif AlertObject.direction == "вниз":
                            await bot.send_message(chat_id=AlertObject.user_id,text=f"ALERT: Цена {AlertObject.val1} c точки {AlertObject.cost} упала на {rasnitsa} {AlertObject.val2}")
            await session.commit()
            await asyncio.sleep(5)


