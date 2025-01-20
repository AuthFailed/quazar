from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def ios_apps():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 Hiddify", callback_data="ios_app_hiddify"),
        ],
        [
            InlineKeyboardButton(text="Streizand", callback_data="ios_app_streizand"),
            InlineKeyboardButton(text="FoxRay", callback_data="ios_app_foxray"),
        ],
        [
            InlineKeyboardButton(text="V2Box", callback_data="ios_app_v2box"),
            InlineKeyboardButton(text="Shadowrocket", callback_data="ios_app_shadowrocket"),
        ],
        [
            InlineKeyboardButton(text="SingBox", callback_data="ios_app_singbox"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_instructions"),
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def android_apps():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 Hiddify", callback_data="android_app_hiddify"),
        ],
        [
            InlineKeyboardButton(text="V2RayNG", callback_data="android_app_v2rayng"),
            InlineKeyboardButton(text="Happ", callback_data="android_app_happ"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_instructions"),
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def windows_apps():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 Hiddify", callback_data="windows_app_hiddify"),
        ],
        [
            InlineKeyboardButton(text="NekoRay", callback_data="windows_app_nekoray"),
            InlineKeyboardButton(text="v2rayN", callback_data="windows_app_v2rayn"),
        ],
        [
            InlineKeyboardButton(text="InvisibleMan", callback_data="windows_app_invisibleman"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_instructions"),
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def back_to_apps(device, sub_link=None):
    device_apps = None
    match device:
        case "ios":
            device_apps = "instructions_ios"
        case "android":
            device_apps = "instructions_android"
        case "windows":
            device_apps = "instructions_windows"
        case "apple":
            device_apps = "instructions_apple"
        case "linux":
            device_apps = "instructions_linux"
        case "androidtv":
            device_apps = "instructions_androidtv"

    buttons = []
    if sub_link:
        buttons.append([
            InlineKeyboardButton(text="😎 Открыть подписку", web_app=WebAppInfo(url=sub_link))
        ])

    buttons.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data=device_apps),
        InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu"),
    ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard
