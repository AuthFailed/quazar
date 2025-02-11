import logging

from aiogram import Bot
from aiohttp import web
from dotenv import load_dotenv
import os

from tgbot.misc.db import get_user


load_dotenv()


async def process_marzban_action(action_data: dict, bot: Bot):
    """Process individual Marzban action"""
    username = action_data.get('username')
    action = action_data.get('action')
    enqueued_at = action_data.get('enqueued_at')

    user_data = await get_user(username)
    
    if action == 'user_updated':
        logging.info(f"User {username} was updated at {enqueued_at}")
        await bot.send_message(user_data['tg_id'], text="Вы были обновлены")
    elif action == 'user_created':
        logging.info(f"New user {username} was created at {enqueued_at}")
        # Add your user creation logic here
    elif action == 'user_deleted':
        logging.info(f"User {username} was deleted at {enqueued_at}")
        # Add your user deletion logic here
    else:
        logging.warning(f"Unknown action {action} for user {username}")

async def handle_marzban_webhook(request, bot):
    """Handle incoming webhook from Marzban"""
    try:
        # Verify webhook secret
        webhook_secret = request.headers.get('x-webhook-secret')
        config_secret =  os.environ.get("WEBHOOK_SECRET")
        
        if not webhook_secret or webhook_secret != config_secret:
            logging.warning("Invalid webhook secret received")
            return web.Response(status=403, text='Invalid secret')

        # Parse webhook data
        data = await request.json()
        
        if not isinstance(data, list):
            logging.error("Expected webhook data to be a list")
            return web.Response(status=400, text='Invalid data format')

        # Process each action in the webhook
        for action_data in data:
            await process_marzban_action(action_data, bot)
        
        return web.Response(status=200, text='OK')
        
    except Exception as e:
        logging.error(f"Error processing Marzban webhook: {e}")
        return web.Response(status=500, text=str(e))