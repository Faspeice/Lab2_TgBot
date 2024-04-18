import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.Bot import router
from app.AlertsBase.models import async_main
from dotenv import load_dotenv
import os
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
async def main():
    await async_main()
    load_dotenv()
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


