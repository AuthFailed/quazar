from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Принятие в канал
def accept_to_channel(user_id):
    buttons = [
        [
            InlineKeyboardButton(text="✔️ Принять",
                                 callback_data="accept_channel"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data="deny_channel"),
        ],
        [
            InlineKeyboardButton(text="✉️ Написать", url=f"https://t.me/{user_id}"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


# Сообщение ливнувшему юзеру
def leaved_user(user_id):
    buttons = [
        [
            InlineKeyboardButton(text="✉️ Написать", url=f"https://t.me/{user_id}"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


# Админ-меню
def admin_menu():
    buttons = [
        [
            InlineKeyboardButton(text="📊 Статус сервера", callback_data="adminmenu_serverstatus")
        ],
        [
            InlineKeyboardButton(text="👨‍👦‍👦 Пользователи", callback_data="adminmenu_users"),
            InlineKeyboardButton(text="🌐 Ноды", callback_data="adminmenu_nodes"),
        ],
        [
            InlineKeyboardButton(text="🌀 Ядро", callback_data="adminmenu_core"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard

def admin_vpn_menu_core():
    buttons = [
        [
            InlineKeyboardButton(text="📝 Конфиг", callback_data="adminmenu_core_xray_config")
        ],
        [
            InlineKeyboardButton(text="🌀 Рестарт", callback_data="adminmenu_core_restartxray")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="adminmenu")
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard

def to_home():
    buttons = [
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="adminmenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard