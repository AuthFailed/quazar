import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
import os

from tgbot.keyboards.user.inline import to_home, usermenu_kb_sub, \
    usermenu_kb_revokesub, usermenu_kb_main, usermenu_kb_changestatus
from tgbot.misc.marzban_api import get_user_by_id, format_bytes, revoke_user_sub, is_user_created, create_user, \
    activate_user, deactivate_user

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

    ready_message = f"""⭐ <b>Квазар | Главное меню</b>

Используй кнопки ниже для управления ботом
"""

    await message.answer(ready_message,
                         reply_markup=usermenu_kb_main())


@user_router.callback_query(F.data == "usermenu")
async def usermenu(callback: CallbackQuery) -> None:
    """Главное меню"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        await callback.answer()
        return

    ready_message = f"""⭐ <b>Квазар | Главное меню</b>

Используй кнопки ниже для управления ботом
"""

    await callback.message.edit_text(ready_message, reply_markup=usermenu_kb_main())
    await callback.answer()


@user_router.callback_query(F.data == "usermenu_sub")
async def usermenu_sub(callback: CallbackQuery) -> None:
    """Меню подписки"""
    await callback.answer("Загружаю подписку...")
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    if not await is_user_created(callback.from_user.id):
        user = await create_user(callback.from_user.id)
    else:
        user = await get_user_by_id(user_id=callback.from_user.id)

    user_status = True if user.status == "active" else False

    ready_message = f"""⭐ <b>Квазар | Главное меню</b>

🎟️ Статус аккаунта: {"✅ Включен" if user_status else "❌ Выключен"}
💿 Месячный трафик: {format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}

<b>Доп. инфо</b>
Трафик за все время: {format_bytes(user.lifetime_used_traffic)}
Технический ID: <code>{user.username}</code>
"""

    await callback.message.edit_text(ready_message,
                                     reply_markup=usermenu_kb_sub(sub_link=user.subscription_url,
                                                                  sub_status=user_status))


@user_router.callback_query(F.data == "usermenu_faq")
async def usermenu_faq(callback: CallbackQuery) -> None:
    """Раздел FAQ"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()

    await callback.message.edit_text("""<b>⭐ Квазар | FAQ</b>

<b>Доступные сервера</b>
🇦🇹 Австрия, Вена - <code>au.quazar.chrsnv.ru</code>
🇸🇪 Швеция, Стокгольм - <code>sw.quazar.chrsnv.ru</code>

<b>Технология</b>
<blockquote expandable>VPN используется протокол VLESS поверх TCP с технологией REALITY - это современное решение для обхода блокировок, которое отлично маскирует трафик под обычные HTTPS-соединения
Дополнительно используются XTLS и Vision для максимальной производительности и скорости работы</blockquote>

<b>Поддержка устройств</b>
Поддерживаются все современные устройства, на которые есть приложения для подключения к VPN. Найти список доступных приложений можно на странице твоей подписки""",
                                     reply_markup=to_home(), disable_web_page_preview=True)



@user_router.callback_query(F.data == "usermenu_changestatus")
async def usermenu_revokesub(callback: CallbackQuery) -> None:
    """Меню изменения статуса аккаунта"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()

    user = await get_user_by_id(user_id=callback.from_user.id)

    activate_message = f"""<b>⭐ Квазар | Включение аккаунта</b>

⚠️ <b>Внимание</b>
Это действие <b>активирует аккаунт</b>
Все подключения - <b>восстановятся, сеть заработает</b>

Выключить аккаунт повторно можно в том же меню"""

    deactivate_message = f"""<b>⭐ Квазар | Отключение аккаунта</b>
    
⚠️ <b>Внимание</b>
Это действие <b>деактивирует аккаунт</b>
Все подключения - <b>перестанут работать</b>, в том числе текущие активные
    
Включить аккаунт обратно можно в том же меню
    
<i>Рекомендуется выполнять это действие если к твоим подключениям кто-то получил доступ</i>"""

    if user.status == "active":
        await callback.message.edit_text(deactivate_message,
                                         reply_markup=usermenu_kb_changestatus())
    else:
        await callback.message.edit_text(activate_message,
                                         reply_markup=usermenu_kb_changestatus())


@user_router.callback_query(F.data == "usermenu_changestatus_agree")
async def usermenu_changestatus(callback: CallbackQuery) -> None:
    """Изменение статуса аккаунта"""
    await callback.answer("Меняю статус аккаунта...")

    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return
    user = await get_user_by_id(user_id=callback.from_user.id)
    user_status = True if user.status == "active" else False

    if user_status:
        new_user = await deactivate_user(callback.from_user.id)
    else:
        new_user = await activate_user(callback.from_user.id)

    new_user_status = True if new_user.status == "active" else False

    ready_message = f"""⭐ <b>Квазар | Главное меню</b>

🎟️ Статус аккаунта: {"✅ Включен" if new_user_status else "❌ Выключен"}
💿 Месячный трафик: {format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}

<b>Доп. инфо</b>
Трафик за все время: {format_bytes(user.lifetime_used_traffic)}
Технический ID: <code>{user.username}</code>
"""

    await callback.message.edit_text(ready_message,
                                     reply_markup=usermenu_kb_sub(sub_link=user.subscription_url,
                                                                  sub_status=new_user_status))


@user_router.callback_query(F.data == "usermenu_revokesub")
async def usermenu_revokesub(callback: CallbackQuery) -> None:
    """Меню обнуления подписки"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()
    await callback.message.edit_text(f"""<b>⭐ Квазар | Обнуление подписки</b>

⚠️ <b>Внимание</b>
Это действие <b>обнулит текущую ссылку на подписку</b>
Все подключения, которые были настроены по текущей ссылке - <b>продолжат работать</b>, но по ней не получится получать обновления серверов

Новую ссылку можно будет получить на странице подписки в главном меню

<i>Рекомендуется выполнять это действие если к твоей ссылке кто-то получил доступ</i>""",
                                     reply_markup=usermenu_kb_revokesub())


@user_router.callback_query(F.data == "usermenu_revokesub_agree")
async def usermenu_revokesub_agree(callback: CallbackQuery) -> None:
    """Обнуление подписки пользователя"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer("Обнуляю подписку...")
    user = await get_user_by_id(user_id=callback.from_user.id)
    user_status = True if user.status == "active" else False
    await revoke_user_sub(user.username)

    ready_message = f"""<b>⭐ Квазар | Главное меню</b>

🎟️ Статус аккаунта: {"✅ Включен" if user_status else "❌ Выключен"}
💿 Месячный трафик: {format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}

<b>Доп. инфо</b>
Трафик за все время: {format_bytes(user.lifetime_used_traffic)}
Технический ID: <code>{user.username}</code>
    """

    await callback.message.edit_text(ready_message, reply_markup=usermenu_kb_main())
