import os
import mariadb
from dotenv import load_dotenv

load_dotenv()


async def get_user(userid: int = "Telegram userid") -> dict:
    user_data = {
        "id": None,
        "username": None,
        "status": None,
        "used_traffic": None,
        "data_limit": None,
        "expire": None,
        "created_at": None,
        "data_limit_reset_strategy": None,
        "note": None,
        "sub_updated_at": None,
        "sub_last_user_agent": None,
        "online_at": None,
        "edit_at": None,
        "on_hold_timeout": None,
        "on_hold_expire_duration": None,
        "auto_delete_in_days": None,
        "last_status_change": None
    }

    try:
        conn = mariadb.connect(
            user=os.environ.get('MARIA_USER'),
            password=os.environ.get('MARIA_PASSWORD'),
            host=os.environ.get('MARIA_HOST'),
            port=int(os.environ.get('MARIA_PORT')),
            database=os.environ.get('MARIA_DATABASE')
        )

        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, status, used_traffic, data_limit, expire, created_at, data_limit_reset_strategy, note, sub_updated_at, sub_last_user_agent, online_at, edit_at, on_hold_timeout, on_hold_expire_duration, auto_delete_in_days, last_status_change FROM users WHERE tgid = ?",
                (userid,))
            node_data = cur.fetchone()

            if node_data:
                for i, key in enumerate(user_data.keys()):
                    user_data[key] = node_data[i]

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    finally:
        conn.close()

    return user_data

async def get_user_traffic(marzbanid: int = "Marzban userid"):
    user_data = {
        "id": None,
        "username": None,
        "status": None,
        "used_traffic": None,
        "data_limit": None,
        "expire": None,
        "created_at": None,
        "data_limit_reset_strategy": None,
        "note": None,
        "sub_updated_at": None,
        "sub_last_user_agent": None,
        "online_at": None,
        "edit_at": None,
        "on_hold_timeout": None,
        "on_hold_expire_duration": None,
        "auto_delete_in_days": None,
        "last_status_change": None
    }

    try:
        conn = mariadb.connect(
            user=os.environ.get('MARIA_USER'),
            password=os.environ.get('MARIA_PASSWORD'),
            host=os.environ.get('MARIA_HOST'),
            port=int(os.environ.get('MARIA_PORT')),
            database=os.environ.get('MARIA_DATABASE')
        )

        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, status, used_traffic, data_limit, expire, created_at, data_limit_reset_strategy, note, sub_updated_at, sub_last_user_agent, online_at, edit_at, on_hold_timeout, on_hold_expire_duration, auto_delete_in_days, last_status_change FROM users WHERE tgid = ?",
                (marzbanid,))
            node_data = cur.fetchone()

            if node_data:
                for i, key in enumerate(user_data.keys()):
                    user_data[key] = node_data[i]

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    finally:
        conn.close()

    return user_data

async def get_nodes_data():
    try:
        conn = mariadb.connect(
            user=os.environ.get('MARIA_USER'),
            password=os.environ.get('MARIA_PASSWORD'),
            host=os.environ.get('MARIA_HOST'),
            port=int(os.environ.get('MARIA_PORT')),
            database=os.environ.get('MARIA_DATABASE')
        )

        with conn.cursor() as cur:
            cur.execute(
                "SELECT name, address, port, api_port, status, last_status_change, xray_version, usage_coefficient FROM nodes")
            node_data = cur.fetchall()
            return node_data

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return []
    finally:
        conn.close()

async def get_reset_date(username):
    try:
        conn = mariadb.connect(
            user=os.environ.get('MARIA_USER'),
            password=os.environ.get('MARIA_PASSWORD'),
            host=os.environ.get('MARIA_HOST'),
            port=int(os.environ.get('MARIA_PORT')),
            database=os.environ.get('MARIA_DATABASE')
        )

        with conn.cursor() as cur:
            cur.execute(
                "SELECT created_at, username FROM users WHERE username = ?", (username,)
            )
            reset_date = cur.fetchone()
            if reset_date[0]:
                return reset_date[0].day

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None
    finally:
        conn.close()