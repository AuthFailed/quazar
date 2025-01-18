from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.admin.inline import admin_menu, admin_vpn_menu_core, to_home
from tgbot.misc.marzban_api import get_system_stats, restart_core, get_core_config

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.answer("⭐ Главное меню <b>Квазар</b>\n\n"
                         "Я - бот проекта Квазар\n"
                         "<i>Используй кнопки ниже для администрирования</i>", reply_markup=admin_menu())


@admin_router.callback_query(F.data == "adminmenu")
async def adminmenu(callback: CallbackQuery) -> None:
    """Главное меню"""
    await callback.answer()

    await callback.message.edit_text("⭐ Главное меню <b>Квазар</b>\n\n"
                         "Я - бот проекта Квазар\n"
                         "<i>Используй кнопки ниже для администрирования</i>", reply_markup=admin_menu())

@admin_router.callback_query(F.data == "adminmenu_serverstatus")
async def adminmenu_serverstatus(callback: CallbackQuery) -> None:
    """Статус сервера"""
    await callback.answer("Проверяю статус сервера...")
    server_stats = await get_system_stats()

    await callback.message.edit_text("⭐ <b>Квазар</b>\n\n"
                                     "<b>Сервер</b>\n"
                                     f"⚡ Память: {server_stats['mem_used']} | {server_stats['mem_total']}\n"
                                     f"🧠 Процессор: {server_stats['cpu_cores']} ядер, нагрузка {server_stats['cpu_usage']}\n\n"
                                     f"<b>Пользователи</b>\n"
                                     f"🧮 Всего: {server_stats['total_user']}\n"
                                     f"🟢 Активно: {server_stats['users_active']}\n\n"
                                     f"<b>Трафик</b>\n"
                                     f"📥 Входящий: {server_stats['incoming_bandwidth']}\n"
                                     f"📤 Исходящий: {server_stats['outgoing_bandwidth']}\n\n"
                                     f"<b>Скорость</b>\n"
                                     f"Вход: {server_stats['incoming_bandwidth_speed']} ⬇️\n"
                                     f"Исход: {server_stats['outgoing_bandwidth_speed']} ⬆️", reply_markup=to_home())

@admin_router.callback_query(F.data == "adminmenu_users")
async def adminmenu_users(callback: CallbackQuery) -> None:
    """Пользователи VPN"""
    await callback.answer("Загружаю данные пользователей...")

@admin_router.callback_query(F.data == "adminmenu_nodes")
async def adminmenu_nodes(callback: CallbackQuery) -> None:
    """Ноды"""
    await callback.answer("Загружаю данные нодов...")

@admin_router.callback_query(F.data == "adminmenu_core")
async def adminmenu_core(callback: CallbackQuery) -> None:
    """Меню управления ядром"""
    await callback.answer()

    await callback.message.edit_text("⭐ <b>Квазар</b>\n\n"
                                     "Меню управления ядром Xray", reply_markup=admin_vpn_menu_core())

@admin_router.callback_query(F.data == "adminmenu_core_xray_config")
async def adminmenu_core_xray_config(callback: CallbackQuery) -> None:
    """Проверка конфига ядра Xray"""
    await callback.answer("Загружаю конфиг ядра...")

    core_config = await get_core_config()
    ready_message = ("⭐ <b>Квазар</b>\n\n"
                     "Конфиг ядра:\n"
                     f"<pre><code>{core_config}</code></pre>")
    await callback.message.edit_text(ready_message, reply_markup=admin_vpn_menu_core())

@admin_router.callback_query(F.data == "adminmenu_core_restartxray")
async def adminmenu_core_restartxray(callback: CallbackQuery) -> None:
    """Рестарт ядра Xray"""
    await restart_core()
    await callback.answer("Ядра на всех нодах успешно перезапущены")
