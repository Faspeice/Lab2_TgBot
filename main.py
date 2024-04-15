import asyncio
import logging
from app.AlertsBase.bdrequests import messageAlerts
from aiogram import Bot, Dispatcher
from BotConfig import TOKEN
from app.Bot import router,rasilka
from app.AlertsBase.models import async_main

bot = Bot(token=TOKEN)
dp = Dispatcher()
async def main():
    await async_main()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


