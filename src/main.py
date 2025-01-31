import asyncio
import os
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from scheduler import start_scheduler

async def main():
    #redis_host = os.getenv('REDIS_HOST', 'localhost')
    #redis_port = int(os.getenv('REDIS_PORT', 6379))
    #redis_password = os.getenv('REDIS_PASSWORD', None)
    #redis = Redis(host='redis', port=6379, password=redis_password)
    #redis = Redis(host='localhost')
    redis = Redis
    redis_url = os.getenv('REDIS_URL')  # например, redis://:<password>@<hostname>:<port>
    redis_client = redis.from_url(redis_url)
    storage = RedisStorage(redis=redis_client)

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    start_scheduler(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())



