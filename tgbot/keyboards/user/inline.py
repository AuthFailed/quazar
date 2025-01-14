from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def user_menu(sub_link="https://google.com"):
    buttons = [
        [
            InlineKeyboardButton(text='Открыть подписку', web_app=WebAppInfo(url=sub_link))
        ],
        [
            InlineKeyboardButton(text="📜 FAQ", callback_data="usermenu_faq"),
            InlineKeyboardButton(text="📜 Инструкции", callback_data="usermenu_instructions"),
        ],
        [
            InlineKeyboardButton(text="Канал", url="https://t.me/+iP94bPGODz4wNGZi"),
            InlineKeyboardButton(text="🚨 Помощь", url="https://t.me/roman_domru"),
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