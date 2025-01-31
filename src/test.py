import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token="7392357856:AAFUwBeOHzS2juVwIWY6z291PEI8IzkhA-4")
dp = Dispatcher()
scheduler = AsyncIOScheduler()

async def send_reminder(user_id: int, text: str):
    await bot.send_message(user_id, text)

async def daily_reminder():
    user_id = 154704188  # Пример ID пользователя
    await send_reminder(user_id, "Не забывайте о вашем напоминании!")

scheduler.add_job(daily_reminder, "interval", minutes=0.5, id="daily_reminder")

@dp.message()
async def on_start(message: Message):
    await message.answer("Бот запущен. Уведомления настроены.")

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

