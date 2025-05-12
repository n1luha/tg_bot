import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main

async def main():
    await async_main()
    bot = Bot(token='7717307277:AAHzDIPsfdaZcTuvPszxZXq4nZ7joHIS1qI')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import sys
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
