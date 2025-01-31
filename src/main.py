import asyncio
import os
from aiogram import Bot, Dispatcher
from src.config import BOT_TOKEN
from src.handlers import router
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from src.scheduler import start_scheduler


async def main():
    # Получаем URL подключения к Redis из переменной окружения
    redis_url = os.getenv('REDIS_URL')  # Например, redis://:<password>@<hostname>:<port>

    if not redis_url:
        raise ValueError("REDIS_URL environment variable is not set")

    # Подключаемся к Redis используя url
    redis_client = Redis.from_url(redis_url)

    # Настройка хранилища для Aiogram
    storage = RedisStorage(redis=redis_client)

    # Создаем бота и диспетчера
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    # Включаем роутер и запускаем планировщик
    dp.include_router(router)
    start_scheduler(bot)

    # Убираем webhook и начинаем опрос
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Запуск приложения
asyncio.run(main())

'''

import asyncio
import os
from aiogram import Bot, Dispatcher
from src.config import BOT_TOKEN
from src.handlers import router
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from src.scheduler import start_scheduler

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

'''

