import os

from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import CallbackQuery, ChatJoinRequest, ChatMemberUpdated
from aiogram import Bot
import logging
from typing import Dict

from datetime import datetime, timedelta

from dotenv import load_dotenv

from tgbot.keyboards.admin.inline import accept_to_channel, leaved_user
from tgbot.keyboards.user.inline import channel_link

load_dotenv()
channel_router = Router()

# Храним входящие запросы
# Формат: {message_id: (chat_id, user_id, timestamp)}
pending_requests: Dict[int, tuple[int, int, datetime]] = {}


@channel_router.chat_join_request()
async def handle_join_request(request: ChatJoinRequest, bot: Bot) -> None:
    """Обрабатываем входящие запросы на вход."""
    user = request.from_user
    chat_id = request.chat.id
    
    # Получаем инфо о пригласительной ссылке
    invite_info = ""
    if request.invite_link:
        invite_info = f"\nПришел по ссылке: <i>{request.invite_link.name if request.invite_link.name else request.invite_link.invite_link}</i>"

    try:
        # Отправка уведомления админу
        admin_msg = await bot.send_message(
            chat_id=os.environ.get("ADMINS"),
            text=f"<b>📩 Новая заявка</b>\n\n"
                 f"Пользователь @{user.username} (ID: <code>{user.id}</code>) оставил запрос на вход в канал{invite_info}",
            reply_markup=accept_to_channel(user_id=user.username)
        )

        pending_requests[admin_msg.message_id] = (chat_id, user.id, datetime.now())

        # Чистим старые запросы (старше 24 часов)
        current_time = datetime.now()
        expired_messages = [
            msg_id for msg_id, (_, _, timestamp) in pending_requests.items()
            if current_time - timestamp > timedelta(hours=24)
        ]
        for msg_id in expired_messages:
            pending_requests.pop(msg_id)

        logging.info(f"Stored join request from {user.username} (ID: {user.id})")

    except Exception as e:
        logging.error(f"Error handling join request: {e}")

@channel_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: ChatMemberUpdated, bot: Bot):
    # Выход из канала
    await deactivate_user(user_id=event.from_user.id)

    await bot.send_message(
        chat_id=os.environ.get("ADMINS"),
        text=f"<b>Выход из канала</b>\nПользователь @{event.from_user.username} (ID: {event.from_user.id}) покинул канал\n"
             f"Аккаунт пользователя деактивирован",
        reply_markup=leaved_user(user_id=event.from_user.username)
    )

    await bot.send_message(
        chat_id=event.from_user.id,
        text=f"""<b>⭐ Квазар | Выход из канала</b>
        
⚠️ <b>Внимание</b>
Аккаунт деактивирован, VPN отключен

Для возобновления доступа требуется подписка на <b>⭐ Квазар</b>

<b>😊 Если подписка уже есть</b>
1. Открой @tribute
2. Открой меню кнопкой внизу
3. Перейди в раздел Подписки - Квазар
4. Нажми на стрелочку сверху и подпишись на канал
5. Вернись сюда и нажми /start

<b>🙁 Если подписки нет/закончилась</b>
1. Открой <a href="https://t.me/tribute/app?startapp=snKl">подписку</a>
2. Выбери способ оплаты и оплати подписку
3. После оплаты перейди в бота @tribute и подпишись на канал
4. Вернись сюда и нажми /start
""",
        reply_markup=channel_link(), disable_web_page_preview=True
    )

@channel_router.callback_query(F.data == "accept_channel")
async def handle_accept_channel(callback: CallbackQuery, bot: Bot) -> None:
    """Подтверждение заявки на вход"""
    try:
        if callback.message.message_id not in pending_requests:
            await callback.answer("Запрос устарел или уже обработан", show_alert=True)
            return

        chat_id, user_id, _ = pending_requests[callback.message.message_id]

        # Подтверждение заявки на вход
        try:
            await bot.approve_chat_join_request(
                chat_id=chat_id,
                user_id=user_id
            )
            logging.info(f"Approved join request for user ID: {user_id}")
        except Exception as e:
            logging.error(f"Failed to approve join request: {e}")
            await callback.answer("Ошибка при одобрении запроса", show_alert=True)
            return

        # Удаление обработанной заявки
        pending_requests.pop(callback.message.message_id)

        message_text = callback.message.text
        await callback.message.edit_text(
            f"{message_text}\n\n✅ Принят администратором {callback.from_user.username}",
            reply_markup=None
        )

        # Уведомление пользователя о подтверждении заявки
        try:
            await bot.send_message(
                chat_id=user_id,
                text="✅ Твоя заявка на вступление в канал была одобрена!"
            )
        except Exception as e:
            logging.error(f"Failed to send approval message to user: {e}")

        await callback.answer("Пользователь успешно принят")

    except Exception as e:
        logging.error(f"Error handling accept channel callback: {e}")
        await callback.answer("Произошла ошибка при обработке запроса", show_alert=True)


@channel_router.callback_query(F.data == "deny_channel")
async def handle_deny_channel(callback: CallbackQuery, bot: Bot) -> None:
    """Отмена заявки на вход"""
    try:
        if callback.message.message_id not in pending_requests:
            await callback.answer("Запрос устарел или уже обработан", show_alert=True)
            return

        chat_id, user_id, _ = pending_requests[callback.message.message_id]

        # Отмена заявки
        try:
            await bot.decline_chat_join_request(
                chat_id=chat_id,
                user_id=user_id
            )
            logging.info(f"Declined join request for user ID: {user_id}")
        except Exception as e:
            logging.error(f"Failed to decline join request: {e}")
            await callback.answer("Ошибка при отклонении запроса", show_alert=True)
            return

        # Удаление обработанной заявки
        pending_requests.pop(callback.message.message_id)

        message_text = callback.message.text
        await callback.message.edit_text(
            f"{message_text}\n\n❌ Отклонен администратором {callback.from_user.username}",
            reply_markup=None
        )

        # Уведомление пользователя об отмене заявки
        try:
            await bot.send_message(
                chat_id=user_id,
                text="❌ Твоя заявка на вступление в канал была отклонена."
            )
        except Exception as e:
            logging.error(f"Failed to send denial message to user: {e}")

        await callback.answer("Пользователь отклонен")

    except Exception as e:
        logging.error(f"Error handling deny channel callback: {e}")
        await callback.answer("Произошла ошибка при обработке запроса", show_alert=True)