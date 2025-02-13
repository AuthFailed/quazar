import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
import os

from tgbot.keyboards.user.inline import to_home, usermenu_kb_sub, \
    usermenu_kb_revokesub, usermenu_kb_main, usermenu_kb_changestatus, setup_pickdevice
from tgbot.keyboards.user.instructions import androidtv_apps, ios_apps, android_apps, windows_apps
# from tgbot.misc.db import get_reset_date
from tgbot.misc.remna_api import format_bytes, get_user_by_tgid, revoke_user_sub, format_date, days_between_unix_timestamp

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

    user = await get_user_by_tgid(tgid=callback.from_user.id)

    sub_status = ""
    match user["status"]:
        case "ACTIVE":
            sub_status = f"""<b>🎫 Подписка</b>: {f"до {format_date(user["expireAt"])}" if user["expireAt"] else "♾️"}
<b>📊 Использовано</b>: {format_bytes(user["usedTrafficBytes"])} из {format_bytes(user["trafficLimitBytes"])}"""
        case "LIMITED":
            sub_status = f"""<b>🎫 Подписка</b>: ❌ Лимит ({user["expire"]})
<b>📊 Использовано</b>: {format_bytes(user["used_traffic"])} из {format_bytes(user["trafficLimitBytes"])}"""
        case "DISABLED":
            sub_status = f"""<b>🎫 Подписка</b>: ❌ Отключена"""
        
        case "EXPIRED":
            sub_status = f"""<b>🎫 Подписка</b>: ❌ Истекла {user["expire"]}"""

    ready_message = f"""⭐ <b>Квазар | Подписка</b>

{sub_status}
<b>♻️ Сброс лимита</b>: каждое 1 число месяца

<b>🔗 Ссылка-подписка для клиента</b>:
<code>{user["subscriptionUrl"]}</code>

<b>Доп. инфо</b>
<b>🚦 Трафик за все время</b>: {format_bytes(user["lifetimeUsedTrafficBytes"])}
<b>⚙️ Технический ID</b>: <code>{user["username"]}</code>
"""
    try:
        await callback.message.edit_text(ready_message,
                                     reply_markup=usermenu_kb_sub(user_status=user["status"]))
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
🇩🇪 Германия, Франкфурт - <code>de.q-access.ru</code>
🇫🇮 Финляндия, Хельсинки - <code>fn.q-access.ru</code>
🇸🇪 Швеция, Стокгольм - <code>sw.q-access.ru</code>

Мультихоп подключения проходят через <code>gw.q-access.ru</code> в России

<b>🦾 Технология</b>
<blockquote expandable>VPN используется протокол VLESS поверх TCP с технологией REALITY - это современное решение для обхода блокировок, которое отлично маскирует трафик под обычные HTTPS-соединения
Дополнительно используются XTLS и Vision для максимальной производительности и скорости работы</blockquote>

<b>🚧 Ограничения</b>
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
async def usermenu_instructions(callback: CallbackQuery, state: FSMContext) -> None:
    """Раздел инструкций"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()
    await state.clear()

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
    elif device == "androidtv":
        message = """<b>⭐ Квазар | Инструкции для AndroidTV</b>

Выбери приложение в списке ниже

Если не знаешь какое выбрать - бери то, что помечено <b>🔥огоньком</b>
Это рекомендуемое приложение для твоего устройства"""

        await callback.message.edit_text(message,
                                         reply_markup=androidtv_apps())

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
    user = await revoke_user_sub(callback.from_user.id)

    sub_status = ""
    match user["status"]:
        case "ACTIVE":
            sub_status = f"""<b>🎫 Подписка</b>: {f"до {format_date(user["expireAt"])}" if user["expireAt"] else "♾️"}
<b>📊 Использовано</b>: {format_bytes(user["usedTrafficBytes"])} из {format_bytes(user["trafficLimitBytes"])}"""
        case "LIMITED":
            sub_status = f"""<b>🎫 Подписка</b>: ❌ Лимит ({user["expire"]})
<b>📊 Использовано</b>: {format_bytes(user["used_traffic"])} из {format_bytes(user["trafficLimitBytes"])}"""
        case "DISABLED":
            sub_status = f"""<b>🎫 Подписка</b>: ❌ Отключена"""
        
        case "EXPIRED":
            sub_status = f"""<b>🎫 Подписка</b>: ❌ Истекла {user["expire"]}"""

    ready_message = f"""⭐ <b>Квазар | Подписка</b>

{sub_status}
<b>♻️ Сброс лимита</b>: каждое 1 число месяца

<b>🔗 Ссылка-подписка для клиента</b>:
<code>{user["subscriptionUrl"]}</code>

<b>Доп. инфо</b>
<b>🚦 Трафик за все время</b>: {format_bytes(user["lifetimeUsedTrafficBytes"])}
<b>⚙️ Технический ID</b>: <code>{user["username"]}</code>
"""
    try:
        await callback.message.edit_text(ready_message,
                                     reply_markup=usermenu_kb_sub(user_status=user["status"]))
    except TelegramBadRequest as e:
        pass