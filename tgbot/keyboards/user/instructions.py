from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def ios_apps():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 Streizand", callback_data="ios_app_streizand"),
        ],
        [
            InlineKeyboardButton(text="V2Box", callback_data="ios_app_v2box"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_setup"),
            InlineKeyboardButton(text="🏠 На главную", callback_data="usermenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def android_apps():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 Happ", callback_data="android_app_happ"),
        ],
        [
            InlineKeyboardButton(text="V2RayNG", callback_data="android_app_v2rayng")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_setup"),
            InlineKeyboardButton(text="🏠 На главную", callback_data="usermenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def windows_apps():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 NekoRay", callback_data="windows_app_nekoray"),
        ],
        [
            InlineKeyboardButton(text="v2rayN", callback_data="windows_app_v2rayn"),
            InlineKeyboardButton(text="InvisibleMan", callback_data="windows_app_invisibleman"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_setup"),
            InlineKeyboardButton(text="🏠 На главную", callback_data="usermenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def androidtv_apps():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 VPN4TV", callback_data="androidtv_app_vpn4tv"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_setup"),
            InlineKeyboardButton(text="🏠 На главную", callback_data="usermenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def back_to_apps(device):
    device_apps = None
    match device:
        case "ios":
            device_apps = "setup_ios"
        case "android":
            device_apps = "setup_android"
        case "windows":
            device_apps = "setup_windows"
        case "apple":
            device_apps = "setup_apple"
        case "linux":
            device_apps = "setup_linux"
        case "androidtv":
            device_apps = "setup_androidtv"

    buttons = []

    buttons.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data=device_apps),
        InlineKeyboardButton(text="🏠 На главную", callback_data="usermenu"),
    ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard
