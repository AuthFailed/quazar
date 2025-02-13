import json
import os
import random
import string
import aiohttp
import requests
from datetime import datetime

import pytz
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("REMNA_URL") + "/api"
headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {os.environ.get("REMNA_TOKEN")}'
}

# Действия с пользователями
async def create_user(user_id):
    """Создание пользователя"""
    
    return new_user

async def get_user_by_tgid(tgid: int):
    api_url = f'{url}/users/v2'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers=headers) as response:
                if response.status != 200:
                    text = await response.text()
                    print(f"Error: {response.status}")
                    print(text)
                    return None

                try:
                    json_response = await response.json()
                    users = json_response.get('response', {}).get('users', [])

                    for user in users:
                        username = user.get('username', '')
                        if str(tgid) in username:
                            return user

                    return None

                except (ValueError, KeyError) as e:
                    print(f"Error processing response: {e}")
                    return None

        except aiohttp.ClientError as e:
            print(f"Error during request: {e}")
            return None

async def revoke_user_sub(tgid):
    """Сброс ссылки на подписку"""
    user = await get_user_by_tgid(tgid)
    api_url = f'{url}/users/revoke/{user['uuid']}'
    print(user)
    print(api_url)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(api_url, headers=headers) as response:
                if response.status != 200:
                    return None

                try:
                    json_response = await response.json()
                    user = json_response.get('response', {})

                    return user

                except (ValueError, KeyError) as e:
                    print(f"Error processing response: {e}")
                    return None

        except aiohttp.ClientError as e:
            print(f"Error during request: {e}")
            return None


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


def format_date(timestamp: str):
    month_map = {
    "Jan": "янв.", "Feb": "фев.", "Mar": "мар.", "Apr": "апр.",
    "May": "мая", "Jun": "июн.", "Jul": "июл.", "Aug": "авг.",
    "Sep": "сен.", "Oct": "окт.", "Nov": "нояб.", "Dec": "дек."
    }

    timestamp = "2029-12-31T11:01:22.952Z"
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Format the date and time
    formatted_date = dt.strftime("%d %b %Y %H:%M")
    for en, ru in month_map.items():
        formatted_date = formatted_date.replace(en, ru)
    return formatted_date


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
    """Calculate days between a Unix timestamp and now in Moscow."""
    moscow_tz = pytz.timezone("Europe/Moscow")
    target_date = datetime.fromtimestamp(unix_timestamp, tz=moscow_tz)
    current_time = datetime.now(moscow_tz)
    days_difference = (target_date.date() - current_time.date()).days
    return format_days(days_difference)  # Assuming format_days is defined

async def activate_tv(uuid, sub):
    url = "https://api.vpn4tv.com/submit"
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Origin': 'https://api.vpn4tv.com',
        'Referer': 'https://api.vpn4tv.com/submit',
        'Sec-Ch-Ua': '"Not=A?Brand";v="99", "Chromium";v="118"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    
    # Create form data
    form = aiohttp.FormData()
    form.add_field('uuid', uuid)
    form.add_field('vpnConfigText', sub)
    form.add_field('vpnConfig', '', 
                   filename='',
                   content_type='application/octet-stream')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form, headers=headers) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    return "<div class=\"mt-3 alert alert-success\" role=\"alert\">" in text and "успешно обработана" in text
                return False
    except aiohttp.ClientError:
        return False