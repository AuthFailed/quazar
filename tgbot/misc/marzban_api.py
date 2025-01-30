import json
import os
import random
import string
from datetime import datetime

import pytz
from dotenv import load_dotenv

from marzban import MarzbanAPI, UserModify, UserCreate, ProxySettings

load_dotenv()


# Действия с пользователями
async def create_user(user_id):
    """Создание пользователя"""
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'),
                                password=os.environ.get('MARZBAN_PASSWORD'))

    new_user = UserCreate(
        username=generate_username(),
        proxies={
            "vless": ProxySettings(
                flow="xtls-rprx-vision",
            )
        },
        inbounds={
            'vless': [
                'VLESS TCP REALITY',
                'RU-DE VLESS TCP REALITY',
                'RU-FN VLESS TCP REALITY',
                'RU-SW VLESS TCP REALITY'
            ]
        },
        status="active",
        data_limit=107374182400,  # 100GB
        note=str(user_id),
        data_limit_reset_strategy="month"
    )
    new_user = await api.add_user(user=new_user, token=token.access_token)
    return new_user


async def is_user_created(user_id):
    user = await get_user_by_id(user_id)
    if user is None:
        return False
    else:
        return user


async def activate_user(user_id):
    """Активация пользователя"""
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'),
                                password=os.environ.get('MARZBAN_PASSWORD'))

    user = await get_user_by_id(user_id)
    username = user.username

    user = await api.modify_user(
        token=token.access_token,
        username=username,
        user=UserModify(status="active")
    )

    await api.close()
    return user


async def deactivate_user(user_id):
    """Деактивация пользователя"""
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'), password=os.environ.get('MARZBAN_PASSWORD'))

    user = await get_user_by_id(user_id)
    username = user.username

    user = await api.modify_user(
        token=token.access_token,
        username=username,
        user=UserModify(status="disabled")
    )

    await api.close()
    return user


async def get_user_by_id(user_id):
    """Получение пользователя по user_id"""
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'), password=os.environ.get('MARZBAN_PASSWORD'))

    users_response = await api.get_users(
        token=token.access_token,
        search=str(user_id),
        limit=1
    )

    await api.close()
    return users_response.users[0] if users_response.users else None


async def revoke_user_sub(user_id):
    """Сброс ссылки на подписку"""
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'), password=os.environ.get('MARZBAN_PASSWORD'))

    api_response = await api.revoke_user_subscription(
        user_id,
        token=token.access_token,
    )
    await api.close()
    return api_response if api_response else None


# Действия с ядром
async def get_system_stats():
    """Функция возвращает json следующего вида:
    {
    "version": "x",
    "mem_total": "x GB",
    "mem_used": "x GB",
    "cpu_cores": x,
    "cpu_usage": "x%",
    "total_user": x,
    "users_active": x,
    "incoming_bandwidth": "x MB",
    "outgoing_bandwidth": "x GB",
    "incoming_bandwidth_speed": "x KB/s",
    "outgoing_bandwidth_speed": "x KB/s"
    }
    """
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'), password=os.environ.get('MARZBAN_PASSWORD'))

    system_stats = await api.get_system_stats(token=token.access_token)
    formatted_stats = format_system_stats(system_stats)

    await api.close()
    return formatted_stats


async def get_core_config():
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'), password=os.environ.get('MARZBAN_PASSWORD'))

    core_config = await api.get_core_config(token=token.access_token)
    formatted_config = json.dumps(core_config, indent=2)
    await api.close()
    return formatted_config


async def restart_core():
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'), password=os.environ.get('MARZBAN_PASSWORD'))

    await api.restart_core(token=token.access_token)
    await api.close()


# Функции-хелперы
def format_bytes(bytes_value):
    """Функция-хелпер
    Переводит байты в читабельный формат
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} TB"


def format_bandwidth_speed(bytes_per_sec):
    """Функция-хелпер
    Переводит байты/сек в читабельный формат
    """
    return format_bytes(bytes_per_sec) + "/s"


def format_system_stats(raw_stats):
    """Функция-хелпер
    Переводит голую стату системы в читабельный формат
    """
    # Parse the raw string into individual components
    stats = {}
    for item in str(raw_stats).split():
        if '=' in item:
            key, value = item.split('=')
            # Try to convert to float/int if possible
            try:
                if '.' in value:
                    stats[key] = float(value)
                else:
                    stats[key] = int(value)
            except ValueError:
                # If conversion fails, store as string (remove quotes if present)
                stats[key] = value.strip("'\"")

    # Format the stats into human-readable format
    formatted_stats = {
        "version": stats["version"],
        "mem_total": format_bytes(stats["mem_total"]),
        "mem_used": format_bytes(stats["mem_used"]),
        "cpu_cores": stats["cpu_cores"],
        "cpu_usage": f"{stats['cpu_usage']}%",
        "total_user": stats["total_user"],
        "users_active": stats["users_active"],
        "incoming_bandwidth": format_bytes(stats["incoming_bandwidth"]),
        "outgoing_bandwidth": format_bytes(stats["outgoing_bandwidth"]),
        "incoming_bandwidth_speed": format_bandwidth_speed(stats["incoming_bandwidth_speed"]),
        "outgoing_bandwidth_speed": format_bandwidth_speed(stats["outgoing_bandwidth_speed"])
    }

    return formatted_stats


def generate_username(length=6):
    characters = string.ascii_letters + string.digits  # содержит a-z, A-Z, 0-9

    return ''.join(random.choice(characters) for _ in range(length))


def format_date(timestamp):
    # Russian month names in genitive case
    months_ru = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]

    # Convert timestamp to datetime
    date = datetime.fromtimestamp(timestamp)

    # Manually create the Russian-formatted date string
    russian_date_string = f"{date.day} {months_ru[date.month - 1]} {date.year}"

    return russian_date_string


def format_days(days):
    """
    Correctly format the number of days in Russian language.

    Args:
        days (int): Number of days

    Returns:
        str: Formatted string with correct Russian grammatical form
    """
    # Handle absolute value to work with both past and future dates
    days = abs(int(days))

    # Russian grammatical rules for days
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день"
    elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
        return f"{days} дня"
    else:
        return f"{days} дней"


def days_between_unix_timestamp(unix_timestamp):
    """
    Calculate the number of days between a Unix timestamp and current date in Moscow.

    Args:
        unix_timestamp (int or float): Unix timestamp in seconds

    Returns:
        str: Formatted string with number of days
    """
    # Create Moscow timezone
    moscow_tz = pytz.timezone('Europe/Moscow')

    # Convert Unix timestamp to datetime
    target_date = datetime.fromtimestamp(unix_timestamp, tz=moscow_tz)

    # Get current time in Moscow
    current_time = datetime.now(moscow_tz)

    # Calculate days difference
    days_difference = (target_date.date() - current_time.date()).days

    return format_days(days_difference)
