import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
import os

from tgbot.keyboards.user.inline import user_menu, to_home
from tgbot.misc.marzban_api import get_user_by_id, format_bytes

user_router = Router()
load_dotenv()


async def is_user_in_channel(user_id: int, bot):
    channel_id = os.environ.get('CHANNEL')
    try:
        sub = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if sub.status != "left":
            return True
        else:
            await bot.send_message(chat_id=user_id, text='<b>Привет 👋</b>\n\n'
                                                         'Для доступа требуется подписка на канал <b>⭐ Квазар</b>\n\n'
                                                         '<b><a href="https://t.me/+iP94bPGODz4wNGZi">Подписаться</a></b>\n\n'
                                                         'После подтверждения заявки вернись в бота и нажми /start',
                                   disable_web_page_preview=True)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    return False


@user_router.message(CommandStart())
async def user_start(message: Message):
    if not await is_user_in_channel(message.from_user.id, bot=message.bot):
        return

    user = await get_user_by_id(user_id=message.from_user.id)
    ready_message = f"""⭐ <b>Квазар | Главное меню</b>

🎟️ Подписка: {"✅ Активна" if user.status == "active" else "❌ Не активна"}
💿 Месячный трафик: {format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}

Трафик за все время: {format_bytes(user.lifetime_used_traffic)}
Технический ID: {user.username}
"""

    await message.answer(ready_message,
                         reply_markup=user_menu(sub_link=user.subscription_url))


@user_router.callback_query(F.data == "usermenu")
async def usermenu(callback: CallbackQuery) -> None:
    """Главное меню"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        await callback.answer()
        return

    user = await get_user_by_id(user_id=callback.from_user.id)
    ready_message = f"""⭐ <b>Квазар | Главное меню</b>

    🎟️ Подписка: {"✅ Активна" if user.status == "active" else "❌ Не активна"}
    💿 Месячный трафик: {format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}

    Трафик за все время: {format_bytes(user.lifetime_used_traffic)}
    Технический ID: <code>{user.username}</code>
    """

    await callback.message.edit_text(ready_message,
                                     reply_markup=user_menu(sub_link=user.subscription_url))
    await callback.answer()


@user_router.callback_query(F.data == "usermenu_faq")
async def usermenu_faq(callback: CallbackQuery) -> None:
    """Раздел FAQ"""
    await callback.message.edit_text("⭐ <b>Квазар | FAQ</b>\n\n"
                                     "<b>Доступные сервера</b>\n"
                                     "Австрия - <code>152.53.109.159</code>\n"
                                     "Швеция - <code>77.221.141.88</code>\n"
                                     "Германия - <code>150.241.99.169</code>\n\n"
                                     "<b>Технология</b>\n"
                                     "<blockquote expandable>VPN используется протокол VLESS поверх TCP с технологией REALITY - это современное решение для обхода блокировок, которое отлично маскирует трафик под обычные HTTPS-соединения\n"
                                     "Дополнительно используются XTLS и Vision для максимальной производительности и скорости работы</blockquote>\n\n"
                                     "<b>Поддержка устройств</b>\n"
                                     "Поддерживаются все современные устройства, на которые есть приложения для подключения к VPN. Найти список доступных приложений можно на странице твоей подписки",
                                     reply_markup=to_home(), disable_web_page_preview=True)
    await callback.answer()
