from aiogram import Router
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from tgbot.handlers.users.user import is_user_in_channel
from tgbot.keyboards.user.instructions import back_to_apps
from tgbot.misc.remna_api import activate_tv, get_user_by_tgid
from aiogram.fsm.context import FSMContext

from tgbot.misc.states import TV_SETUP



user_instructions = Router()
load_dotenv()


@user_instructions.callback_query(lambda c: c.data.startswith("ios_app_"))
async def ios_app_instructions(callback: CallbackQuery) -> None:
    """Инструкции для iOS"""
    await callback.answer()

    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    user = await get_user_by_tgid(callback.from_user.id)

    app = callback.data.split('_')[2]
    device = callback.data.split('_')[0]

    message = ""
    if app == "streizand":
        message = f"""<b>⭐ Квазар | Инструкция для iOS</b>

<b>👨‍🔧 Установка Streizand</b>
1. Установи приложение <a href="https://apps.apple.com/ru/app/streisand/id6450534064">Streizand</a>
2. Скопируй ссылку
<blockquote><code>{user["subscriptionUrl"]}</code></blockquote>
3. В приложении нажми на плюсик справа сверху и выбери <b>Добавить из буфера</b>
    """
    elif app == "v2box":
        message = f"""<b>⭐ Квазар | Инструкция для iOS</b>

<b>👨‍🔧 Установка v2box</b>
1. Установи приложение <a href="https://apps.apple.com/ru/app/v2box-v2ray-client/id6446814690">v2box</a>
2. Скопируй ссылку
<blockquote><code>{user["subscriptionUrl"]}</code></blockquote>
3. В приложении открой снизу раздел Configs
4. Нажми на плюсик справа сверху и выбери <b>import v2ray uri from clipboard</b>
    """
    await callback.message.edit_text(message, reply_markup=back_to_apps(device=device),
                                     disable_web_page_preview=True)


@user_instructions.callback_query(lambda c: c.data.startswith("android_app_"))
async def android_app_instructions(callback: CallbackQuery) -> None:
    """Инструкции для Android"""
    await callback.answer()

    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    user = await get_user_by_tgid(callback.from_user.id)

    app = callback.data.split('_')[2]
    device = callback.data.split('_')[0]

    message = ""
    if app == "v2rayng":
        message = f"""<b>⭐ Квазар | Инструкция для Android</b>

<b>👨‍🔧 Установка v2rayNG</b>
1. Установи приложение <a href="https://play.google.com/store/apps/details?id=com.v2ray.ang">v2rayNG</a>
2. Скопируй ссылку
<blockquote><code>{user["subscriptionUrl"]}</code></blockquote>
3. В приложении нажми на три точки справа сверху и выбери <code>Обновить подписку группы</code>
"""
    elif app == "happ":
        message = f"""<b>⭐ Квазар | Инструкция для Android</b>

<b>👨‍🔧 Установка Happ</b>
1. Установи приложение <a href="https://github.com/FlyFrg/Happ_android_update/releases/latest/download/Happ.apk">Happ</a>
2. Скопируй ссылку
<blockquote><code>{user["subscriptionUrl"]}</code></blockquote>
3. В приложении нажми на плюсик справа сверху и выбери <b>Вставить из буфера обмена</b>
"""
    await callback.message.edit_text(message, reply_markup=back_to_apps(device=device),
                                     disable_web_page_preview=True)


@user_instructions.callback_query(lambda c: c.data.startswith("windows_app_"))
async def android_app_instructions(callback: CallbackQuery) -> None:
    """Инструкции для Windows"""
    await callback.answer()

    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    user = await get_user_by_tgid(callback.from_user.id)

    app = callback.data.split('_')[2]
    device = callback.data.split('_')[0]

    message = ""
    
    if app == "nekoray":
        message = """<b>⭐ Квазар | Инструкция для Windows</b>

<b>👨‍🔧 Установка Nekoray</b>
1. Установи программу <a href="https://github.com/MatsuriDayo/nekoray/releases/download/4.0.1/nekoray-4.0.1-2024-12-12-windows64.zip">Nekoray</a>
2. Скопируй ссылку
<blockquote><code>{user["subscriptionUrl"]}</code></blockquote>
3. В программе нажми правой кнопкой мыши по пустому месту - <b>Добавить профиль из буфера обмена</b> - <b>Добавить в эту группу</b>

<b>📋 Дополнительно</b>
Доп. инструкции для программы

<b>🤔 Режим подключения</b>
<blockquote expandable><b>🌎 Режим TUN</b>
Активный режим TUN перенаправляет весь сетевой трафик устройства через VPN. Это обеспечивает полное проксирование абсолютно всех подключений

<b>🔀 Режим системного прокси</b>
Активный режим системного прокси включает прокси-сервер на устройстве, что позволяет перенаправлять только конкретные приложения через VPN. Обязательна поддержка прокси со стороны приложения 
</blockquote>

<b>🎌 Маршруты</b>
<blockquote expandable><b>Настройка для Discord</b>
1. Открой раздел <b>Настройка</b> - <b>Настройки маршрутов</b> - <b>Базовые маршруты</b> - <b>Кастомные маршруты</b>
2. Вставь конфигурацию:
<code>{
  "rules": [
    {
      "outbound": "proxy",
      "process_name": [
        "Discord.exe",
        "Update.exe"
      ]
    }
  ]
}</code> 
и нажми ОК
3. <b>Outbound по умолчанию</b> выбери <b>bypass</b>
4. Зайди в <b>Настройка</b> - <b>Настройки маршрутов</b> - <b>Общие</b>
5. Выбери в пунктах <b>Стратегия доменов</b> и <b>Стратегия выбора адреса сервера</b> параметр "ipv4_only"

Нажми ОК и проверь работу Discord при активном подключении</blockquote>
"""
    elif app == "v2rayn":
        message = """<b>⭐ Квазар | Инструкция для Windows</b>

<b>👨‍🔧 Установка v2RayN</b>
1. Скачай <a href="https://github.com/2dust/v2rayN/releases/download/7.4.2/v2rayN-windows-64-SelfContained-With-Core.7z">архив программы</a>
2. Распакуй архив в удобное место, запусти <b>v2rayN.exe</b>
3. Скопируй ссылку
<blockquote><code>{user["subscriptionUrl"]}</code></blockquote>
4. В программе вставь подписку с помощью комбинации ctrl+v
5. Обнови подписку нажав на <b>Subscription Group</b> - <b>Update Subscriptions without proxy</b>

<b>📋 Дополнительно</b>
Доп. инструкции для программы

<b>🤔 Режим подключения</b>
<blockquote expandable><b>🌎 Режим TUN</b>
Активный режим TUN перенаправляет весь сетевой трафик устройства через VPN. Это обеспечивает полное проксирование абсолютно всех подключений

<b>🔀 Режим системного прокси</b>
Активный режим системного прокси включает прокси-сервер на устройстве, что позволяет перенаправлять только конкретные приложения через VPN. Обязательна поддержка прокси со стороны приложения 
</blockquote>

<b>🎌 Регион</b>
<blockquote expandable><b>💫 Смена региона</b>
1. Сверху открой раздел <b>Settings</b> - <b>Regional presets setting</b> и выбери <b>Russia</b>
2. Снизе в окне программы есть выбор Routing:
- Всё - Весь трафик проксируется и идет через VPN
- Всё, кроме РФ - Весь трафик проксируется, кроме торрентов и всех российских IP</blockquote>
"""
    await callback.message.edit_text(message, reply_markup=back_to_apps(device=device),
                                     disable_web_page_preview=True)
    
@user_instructions.callback_query(lambda c: c.data.startswith("androidtv_app_"))
async def android_app_instructions(callback: CallbackQuery, state: FSMContext) -> None:
    """Инструкции для Android"""
    await callback.answer()
    
    if not await is_user_in_channel(callback.from_user.id, bot=callback.bot):
        return

    app = callback.data.split('_')[2]
    device = callback.data.split('_')[0]

    message = ""
    if app == "vpn4tv":
        await state.set_state(TV_SETUP.CODE)
        message = f"""<b>⭐ Квазар | Инструкция для VPN4TV</b>

<b>👨‍🔧 Установка VPN4TV</b>
1. Установи приложение <a href="https://play.google.com/store/apps/details?id=com.vpn4tv.hiddify">VPN4TV</a>
2. Зайди в приложение, найди на экране 10-значный код
3. Напиши его в этот чат сообщением
"""

    await callback.message.edit_text(message, reply_markup=back_to_apps(device=device),
                                     disable_web_page_preview=True)


@user_instructions.message(TV_SETUP.CODE)
async def proccess_tv_setup(message: Message, state: FSMContext):
    if not await is_user_in_channel(message.from_user.id, bot=message.bot):
        return

    await state.clear()
    user = await get_user_by_tgid(message.chat.id)
    activate_status = await activate_tv(uuid=user['uuid'], sub=user["subscriptionUrl"])
    if activate_status: message.answer("Успешно активировали ключ, подожди минутку")
    await message.bot.delete_message(message.chat.id, message.message_id)