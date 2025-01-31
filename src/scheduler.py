from apscheduler.schedulers.asyncio import AsyncIOScheduler
from keyboards import create_quests_keyboard


scheduler = AsyncIOScheduler()


async def send_reminder(bot, user_id, quests):
    # Отправляем сообщение с невыполненными квестами
    await bot.send_message(
        user_id,
        text='Невыполненные квесты:',
        reply_markup=create_quests_keyboard(
            *[quest_name for quest_name in quests]
        )
    )

    # Отправляем сообщение с отметками статуса
    await bot.send_message(
        user_id,
        text='Отметьте статус:',
        reply_markup=create_quests_keyboard(
            *[quest_name + ' ' + quest_status for quest_name, quest_status in quests.items()]
        )
    )


async def daily_reminder(bot):
    from storage import users_db
    for user_id in users_db:
        user_quests = users_db[user_id]
        incomplete_quests = {}
        for quest_name, quest_status in user_quests.items():
            if quest_status == '❌':
                incomplete_quests[quest_name] = quest_status
        await send_reminder(bot, user_id, incomplete_quests)


def start_scheduler(bot):
    scheduler.add_job(daily_reminder, "interval", minutes=10, args=[bot], id="daily_reminder")
    scheduler.start()
