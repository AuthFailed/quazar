from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def usermenu_kb_main():
    buttons = [
        [
            InlineKeyboardButton(text='😎 Подписка', callback_data="usermenu_sub")
        ],
        [
            InlineKeyboardButton(text="📜 FAQ", callback_data="usermenu_faq"),
            InlineKeyboardButton(text="📜 Инструкции", callback_data="usermenu_instructions"),
        ],
        [
            InlineKeyboardButton(text="📡 Канал", url="https://t.me/+LUD7ZdTFBrwxMTli"),
            InlineKeyboardButton(text="🚨 Помощь", url="https://t.me/roman_domru"),
        ],

    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def usermenu_kb_sub(sub_link="https://google.com", sub_status: bool = True):
    buttons = [
        [
            InlineKeyboardButton(text='😎 Открыть подписку', web_app=WebAppInfo(url=sub_link))
        ],
        [
            InlineKeyboardButton(text='🔄 Обновить данные', callback_data="usermenu_sub")
        ],
        [
            InlineKeyboardButton(text="🔽 Выключить",
                                 callback_data="usermenu_changestatus") if sub_status else InlineKeyboardButton(
                text="🔼 Включить", callback_data="usermenu_changestatus"),
            InlineKeyboardButton(text='🔥 Сбросить', callback_data="usermenu_revokesub")
        ],
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu"),
        ]
    ]

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


def channel_link():
    buttons = [
        [
            InlineKeyboardButton(text="📡 Подписаться", url="https://t.me/+LUD7ZdTFBrwxMTli"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


def to_home():
    buttons = [
        [
            InlineKeyboardButton(text="🏠 Домой", callback_data="usermenu"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard
