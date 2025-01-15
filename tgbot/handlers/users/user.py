import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
import os

from tgbot.keyboards.user.inline import user_menu, to_home, user_revoke_sub
from tgbot.misc.marzban_api import get_user_by_id, format_bytes, revoke_user_sub

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
                                                         '<b><a href="https://t.me/+LUD7ZdTFBrwxMTli">Подписаться</a></b>\n\n'
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

🎟️ Доступ: {"✅ Есть" if user.status == "active" else "❌ Нет"}
💿 Месячный трафик: {format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}

<b>Доп. инфо</b>
Трафик за все время: {format_bytes(user.lifetime_used_traffic)}
Технический ID: <code>{user.username}</code>
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

🎟️ Доступ: {"✅ Есть" if user.status == "active" else "❌ Нет"}
💿 Месячный трафик: {format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}

<b>Доп. инфо</b>
Трафик за все время: {format_bytes(user.lifetime_used_traffic)}
Технический ID: <code>{user.username}</code>
"""

    await callback.message.edit_text(ready_message,
                                     reply_markup=user_menu(sub_link=user.subscription_url))
    await callback.answer()


@user_router.callback_query(F.data == "usermenu_faq")
async def usermenu_faq(callback: CallbackQuery) -> None:
    """Раздел FAQ"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        await callback.answer()
        return

    await callback.message.edit_text("""⭐ <b>Квазар | FAQ</b>

<b>Доступные сервера</b>
🇦🇹 Австрия - <code>152.53.109.159</code>
🇸🇪 Швеция - <code>77.221.141.88</code>

<b>Технология</b>
<blockquote expandable>VPN используется протокол VLESS поверх TCP с технологией REALITY - это современное решение для обхода блокировок, которое отлично маскирует трафик под обычные HTTPS-соединения
Дополнительно используются XTLS и Vision для максимальной производительности и скорости работы</blockquote>

<b>Поддержка устройств</b>
Поддерживаются все современные устройства, на которые есть приложения для подключения к VPN. Найти список доступных приложений можно на странице твоей подписки""",
                                     reply_markup=to_home(), disable_web_page_preview=True)
    await callback.answer()


@user_router.callback_query(F.data == "usermenu_revokesub")
async def usermenu_revokesub(callback: CallbackQuery) -> None:
    """Меню обнуления подписки"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        await callback.answer()
        return

    await callback.message.edit_text(f"""⭐ <b>Квазар | Обнуление подписки</b>

⚠️ <b>Внимание</b>
Это действие <b>обнулит текущую ссылку на подписку</b>
Все подключения, которые были настроены по текущей ссылке - <b>продолжат работать</b>, но по ней не получится получать обновления серверов

Новую ссылку можно будет получить на странице подписки в главном меню

<i>Рекомендуется выполнять это действие если к твоей ссылки кто-то получил доступ</i>""", reply_markup=user_revoke_sub())
    await callback.answer()


@user_router.callback_query(F.data == "usermenu_revokesub_agree")
async def usermenu_revokesub_agree(callback: CallbackQuery) -> None:
    """Обнуление подписки пользователя"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        await callback.answer()
        return

    user = await get_user_by_id(user_id=callback.from_user.id)
    api_response = await revoke_user_sub(user.username)

    ready_message = f"""⭐ <b>Квазар | Главное меню</b>

🎟️ Доступ: {"✅ Есть" if user.status == "active" else "❌ Нет"}
💿 Месячный трафик: {format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}

<b>Доп. инфо</b>
Трафик за все время: {format_bytes(user.lifetime_used_traffic)}
Технический ID: <code>{user.username}</code>
    """

    await callback.message.edit_text(ready_message, reply_markup=user_menu(sub_link=api_response.subscription_url))
    await callback.answer("Ссылка на подписку обнулена")