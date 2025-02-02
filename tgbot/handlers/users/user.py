import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
import os

from tgbot.keyboards.user.inline import to_home, usermenu_kb_sub, \
    usermenu_kb_revokesub, usermenu_kb_main, usermenu_kb_changestatus, setup_pickdevice
from tgbot.keyboards.user.instructions import ios_apps, android_apps, windows_apps
from tgbot.misc.db import get_reset_date
from tgbot.misc.marzban_api import get_user_by_id, format_bytes, revoke_user_sub, is_user_created, create_user, \
    activate_user, deactivate_user, format_date, days_between_unix_timestamp

user_router = Router()
load_dotenv()


async def is_user_in_channel(user_id: int, bot):
    channel_id = os.environ.get('CHANNEL')
    try:
        sub = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if sub.status != "left":
            return True
        else:
            await bot.send_message(chat_id=user_id, text="""<b>Привет 👋</b>

Для доступа требуется подписка на <b>⭐ Квазар</b>

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
4. Вернись сюда и нажми /start""", disable_web_page_preview=True)
            return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")


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

    reset_date = await get_reset_date(user.username)

    sub_status = ""
    match user.status:
        case "active":
            sub_status = f"""🎫 Подписка: {format_date(user.expire) + f' ({days_between_unix_timestamp(user.expire)})' if user.expire else "♾️"}
💿 Лимит: <b>{format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}</b>
♻️ Сброс лимита: <b>каждое {reset_date} число месяца</b>"""
        case "disabled":
            sub_status = f"""🎫 Подписка: <b>❌ Отключена</b>"""
        case "limited":
            sub_status = f"""🎫 Подписка: <b>❌ Лимит</b> ({format_date(user.expire)})
💿 Лимит: <b>{format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}</b>
♻️ Сброс лимита: <b>каждое {reset_date} число месяца</b>"""
        case "expired":
            sub_status = f"""🎫 Подписка: <b>❌ Истекла {format_date(user.expire)}</b>"""
        case "on_hold":
            sub_status = f"""🎫 Подписка: <b>⏳ На проверке</b> ({format_date(user.expire)})"""

    ready_message = f"""⭐ <b>Квазар | Подписка</b>

{sub_status}

<b>Доп. инфо</b>
🚦 Трафик за все время: <b>{format_bytes(user.lifetime_used_traffic)}</b>
⚙️ Технический ID: <code>{user.username}</code>
"""
    try:
        await callback.message.edit_text(ready_message,
                                     reply_markup=usermenu_kb_sub(sub_link=user.subscription_url, user_status=user.status))
    except TelegramBadRequest as e:
        pass


@user_router.callback_query(F.data == "usermenu_faq")
async def usermenu_faq(callback: CallbackQuery) -> None:
    """Раздел О проекте"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()

    ready_message = """<b>⭐ Квазар | О проекте</b>

<b>🌐 Локации</b>
🇩🇪 Германия, Франкфурт - <code>.q-access.ru</code>
🇫🇮 Финляндия, Хельсинки - <code>fn.q-access.ru</code>
🇸🇪 Швеция, Стокгольм - <code>sw.q-access.ru</code>

Мультихоп подключения проходят через gw.q-access.ru в России

<b>🦾 Технология</b>
<blockquote expandable>VPN используется протокол VLESS поверх TCP с технологией REALITY - это современное решение для обхода блокировок, которое отлично маскирует трафик под обычные HTTPS-соединения
Дополнительно используются XTLS и Vision для максимальной производительности и скорости работы</blockquote>

<b>🚧 Ограничения</b>
- Одновременно подключенных устройств - <b>не более 3</b>
<i>Автоматически отключается аккаунт</i>
- Использование торрентов
<i>Автоматически блокируется аккаунт на 10 минут</i>"""

    await callback.message.edit_text(ready_message,
                                     reply_markup=to_home(), disable_web_page_preview=True)


@user_router.callback_query(F.data == "usermenu_setup")
async def usermenu_instructions(callback: CallbackQuery) -> None:
    """Раздел подключения"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()

    await callback.message.edit_text("""<b>⭐ Квазар | Выбор устройства</b>

Выбери свое устройство для просмотра инструкции по подключению""",
                                     reply_markup=setup_pickdevice())


@user_router.callback_query(lambda c: c.data.startswith("setup_"))
async def usermenu_instructions(callback: CallbackQuery) -> None:
    """Раздел инструкций"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()

    device = callback.data.split('_')[1]
    if device == "ios":
        message = """<b>⭐ Квазар | Инструкции для iOS</b>
        
Выбери приложение в списке ниже

Если не знаешь какое выбрать - бери то, что помечено <b>🔥огоньком</b>
Это рекомендуемое приложение для твоего устройства"""

        await callback.message.edit_text(message,
                                     reply_markup=ios_apps())
    elif device == "android":
        message = """<b>⭐ Квазар | Инструкции для Android</b>

Выбери приложение в списке ниже

Если не знаешь какое выбрать - бери то, что помечено <b>🔥огоньком</b>
Это рекомендуемое приложение для твоего устройства"""

        await callback.message.edit_text(message,
                                         reply_markup=android_apps())
    elif device == "windows":
        message = """<b>⭐ Квазар | Инструкции для Windows</b>

Выбери приложение в списке ниже

Если не знаешь какое выбрать - бери то, что помечено <b>🔥огоньком</b>
Это рекомендуемое приложение для твоего устройства"""

        await callback.message.edit_text(message,
                                         reply_markup=windows_apps())

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
    await revoke_user_sub(user.username)

    reset_date = await get_reset_date(user.username)

    sub_status = ""
    match user.status:
        case "active":
            sub_status = f"""🎫 Подписка: {format_date(user.expire) + f' ({days_between_unix_timestamp(user.expire)})' if user.expire else "♾️"}
💿 Лимит: <b>{format_bytes(user.used_traffic)} / {format_bytes(user.data_limit)}</b>
♻️ Сброс лимита: <b>каждое {reset_date} число месяца</b>"""
        case "disabled":
            sub_status = f"""🎫 Подписка: <b>❌ Отключена</b>"""
        case "limited":
            sub_status = f"""🎫 Подписка: <b>❌ Лимит</b>
♻️ Сброс лимита: <b>каждое {reset_date} число месяца</b>"""
        case "expired":
            sub_status = f"""🎫 Подписка: <b>❌ Истекла</b>"""
        case "on_hold":
            sub_status = f"""🎫 Подписка: <b>⏳ На проверке</b>"""

    ready_message = f"""⭐ <b>Квазар | Подписка</b>

{sub_status}

<b>Доп. инфо</b>
🚦 Трафик за все время: <b>{format_bytes(user.lifetime_used_traffic)}</b>
⚙️ Технический ID: <code>{user.username}</code>
    """

    try:
        await callback.message.edit_text(ready_message, reply_markup=usermenu_kb_sub(sub_link=user.subscription_url, user_status=user.status))
    except TelegramBadRequest as e:
        pass