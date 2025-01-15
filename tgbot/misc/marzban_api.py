import json
import logging
import os
from dataclasses import asdict

from dotenv import load_dotenv

from marzban import MarzbanAPI

load_dotenv()


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


async def get_user_by_id(user_id):
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
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'), password=os.environ.get('MARZBAN_PASSWORD'))

    api_response = await api.revoke_user_subscription(
        user_id,
        token=token.access_token,
    )
    await api.close()
    return api_response if api_response else None


async def restart_core():
    api = MarzbanAPI(base_url=os.environ.get('MARZBAN_URL'))
    token = await api.get_token(username=os.environ.get('MARZBAN_LOGIN'), password=os.environ.get('MARZBAN_PASSWORD'))

    await api.restart_core(token=token.access_token)
    await api.close()


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
