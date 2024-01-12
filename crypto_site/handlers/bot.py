import telebot
import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
chat_id = os.getenv('chat_id')


def send_notify(message):
	bot = telebot.TeleBot(API_TOKEN)
	bot.send_message(chat_id, message)