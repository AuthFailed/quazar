import logging
import os

from aiogram import Router
from dotenv import load_dotenv

inline_router = Router()
load_dotenv()

async def is_user_in_channel(user_id: int, bot):
    channel_id = os.environ.get('CHANNEL')
    try:
        sub = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        logging.info(sub)
        return sub.status != "left"
    except Exception as e:
        print(f"Произошла ошибка при проверке подписки: {e}")
        return False