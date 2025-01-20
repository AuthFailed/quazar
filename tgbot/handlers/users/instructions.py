from aiogram import Router
from aiogram.types import CallbackQuery
from dotenv import load_dotenv

from tgbot.handlers.users.user import is_user_in_channel
from tgbot.keyboards.user.instructions import back_to_apps
from tgbot.misc.marzban_api import get_user_by_id

user_instructions = Router()
load_dotenv()


@user_instructions.callback_query(lambda c: c.data.startswith("ios_app_"))
async def ios_app_instructions(callback: CallbackQuery) -> None:
    """Инструкции для iOS"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()

    app = callback.data.split('_')[2]
    device = callback.data.split('_')[0]
    user = await get_user_by_id(user_id=callback.from_user.id)

    message = ""
    if app == "hiddify":
        message = f"""<b>⭐ Квазар | Инструкция для iOS</b>

<b>👨‍🔧 Установка Hiddify</b>
1. Установи приложение <a href="https://apps.apple.com/us/app/hiddify-proxy-vpn/id6596777532">Hiddify</a>
2. Запусти приложение, выбери регион по инструкции ниже
3. Открой подписку, найди iOS - Hiddify и нажми <code>Добавить в приложение</code>

<b>🎌 Выбор региона</b>
1. Регион Россия: Российские адреса/сайты - <b>без VPN</b>, остальное - <b>через VPN</b>
2. Регион Другой: Все адреса/сайты <b>через VPN</b>
"""

    await callback.message.edit_text(message, reply_markup=back_to_apps(device=device, sub_link=user.subscription_url),
                                     disable_web_page_preview=True)


@user_instructions.callback_query(lambda c: c.data.startswith("android_app_"))
async def android_app_instructions(callback: CallbackQuery) -> None:
    """Инструкции для Android"""
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    await callback.answer()

    app = callback.data.split('_')[2]
    device = callback.data.split('_')[0]
    user = await get_user_by_id(user_id=callback.from_user.id)

    message = ""
    if app == "hiddify":
        message = f"""<b>⭐ Квазар | Инструкция для Android</b>

<b>👨‍🔧 Установка Hiddify</b>
1. Установи приложение <a href="https://play.google.com/store/apps/details?id=app.hiddify.com">Hiddify</a>
2. Запусти приложение, выбери регион по инструкции ниже
3. Открой подписку, найди Android - Hiddify и нажми <code>Добавить в приложение</code>

<b>🎌 Выбор региона</b>
1. Россия: Российские адреса/сайты - <b>без VPN</b>, остальное - <b>через VPN</b>
2. Другой: Все адреса/сайты <b>через VPN</b>
"""
    elif app == "v2rayng":
        message = f"""<b>⭐ Квазар | Инструкция для Android</b>

<b>👨‍🔧 Установка v2rayNG</b>
1. Установи приложение <a href="https://play.google.com/store/apps/details?id=com.v2ray.ang">v2rayNG</a>
2. Открой подписку, найди Android - V2RayNG и нажми <code>Добавить в приложение</code>
3. В приложении нажми на три точки справа сверху и выбери <code>Обновить подписку группы</code>
"""
    elif app == "happ":
        message = f"""<b>⭐ Квазар | Инструкция для Android</b>

<b>👨‍🔧 Установка Happ</b>
1. Установи приложение <a href="https://github.com/FlyFrg/Happ_android_update/releases/latest/download/Happ.apk">Happ</a>
2. Открой подписку, нажми сверху <b>Скопировать подписку</b>
3. В приложении нажми на плюсик справа сверху и выбери <b>Вставить из буфера обмена</b>
"""
    await callback.message.edit_text(message, reply_markup=back_to_apps(device=device, sub_link=user.subscription_url),
                                     disable_web_page_preview=True)
