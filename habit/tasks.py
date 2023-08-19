
from django.conf import settings
from telebot import TeleBot
from config.celery import app
from habit.models import Habit


@app.task
def send_telegram_message(habit_id):
    habit = Habit.objects.get(id=habit_id)
    bot = TeleBot(settings.TG_BOT_TOKEN)
    message = f"Напоминание о выполнении привычки {habit.action} в " \
              f"{habit.time} в {habit.place}"
    bot.send_message(habit.owner.chat_id, message)

