from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def usermenu_kb_main():
    buttons = [
        [
            InlineKeyboardButton(text='😎 Подписка', callback_data="usermenu_sub")
        ],
        [
            InlineKeyboardButton(text="🔌 Подключение", callback_data="usermenu_setup"),
            # InlineKeyboardButton(text="📜 Инструкции", callback_data="usermenu_instructions"),
        ],
        [
            InlineKeyboardButton(text="🔎 О проекте", callback_data="usermenu_faq"),
            InlineKeyboardButton(text="🌀 Статус", web_app=WebAppInfo(url="https://status.q-access.ru/status/quazar")),
        ],
        [
            InlineKeyboardButton(text="📡 Канал", url="https://t.me/+MdKJNt3W6K01YmJi"),
            InlineKeyboardButton(text="🚨 Поддержка", url="https://t.me/quazar_supp"),
        ],

    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def usermenu_kb_sub(user_status: str, sub_link: str = "https://google.com"):
    buttons = []
    if user_status == "active":
        buttons.extend([
            [
                InlineKeyboardButton(text='😎 Открыть подписку', web_app=WebAppInfo(url=sub_link))
            ],
            [
                InlineKeyboardButton(text='⬆️ Лимит', url="https://t.me/tribute/app?startapp=djXK"),
                InlineKeyboardButton(text='💳 Оплата', url="https://t.me/tribute/app?startapp=snKl")
            ]
        ])
    elif user_status == "disabled" or user_status == "on_hold":
        buttons.append([
            InlineKeyboardButton(text='🚨 Поддержка', url="https://t.me/quazar_supp")
        ])
    elif user_status == "limited":
        buttons.append([
            InlineKeyboardButton(text='⬆️ Увеличить лимит', url="https://t.me/tribute/app?startapp=djXK")
        ])
    elif user_status == "expired":
        buttons.append([
            InlineKeyboardButton(text='💳 Оплатить', url="https://t.me/tribute/app?startapp=snKl")
        ])

    buttons.extend([
        [
            InlineKeyboardButton(text='🔄 Обновить', callback_data="usermenu_sub"),
            InlineKeyboardButton(text='🔥 Сбросить', callback_data="usermenu_revokesub")
        ],
        [
            InlineKeyboardButton(text="🏠 На главную", callback_data="usermenu"),
        ]
    ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def usermenu_kb_changestatus():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 Подтвердить", callback_data="usermenu_changestatus_agree"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_sub"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def usermenu_kb_revokesub():
    buttons = [
        [
            InlineKeyboardButton(text="🔥 Подтвердить", callback_data="usermenu_revokesub_agree"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu_sub"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def setup_pickdevice():
    buttons = [
        [
            InlineKeyboardButton(text="📱 iPhone / iPad", callback_data="setup_ios"),
            InlineKeyboardButton(text="🤖 Android", callback_data="setup_android"),
        ],
        [
            InlineKeyboardButton(text="🖥 Windows", callback_data="setup_windows"),
            InlineKeyboardButton(text="💻 Apple (нет)", callback_data="setup_apple"),
        ],
        [
            InlineKeyboardButton(text="📱 Linux (нет)", callback_data="setup_linux"),
            InlineKeyboardButton(text="📺 AndroidTV (нет)", callback_data="setup_androidtv"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="usermenu"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def channel_link():
    buttons = [
        [
            InlineKeyboardButton(text="📡 Подписаться", url="https://t.me/tribute/app?startapp=snKl"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def to_home():
    buttons = [
        [
            InlineKeyboardButton(text="🏠 На главную", callback_data="usermenu"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard
