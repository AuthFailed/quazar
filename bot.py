import asyncio
import logging
from aiohttp import web
import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.misc.webhook import handle_marzban_webhook
from tgbot.services import broadcaster

WEBHOOK_URL = "https://127.0.0.1/webhook"
WEBHOOK_PATH = "/webhook"
PORT = 7070


async def start_webhook_server(host: str, port: int, bot: Bot):
    app = web.Application()
    # app.router.add_post('/webhook/marzban', handle_marzban_webhook(bot=bot))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    
    await site.start()
    logging.info(f"Webhook server is running on http://{host}:{port}")

async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Bot started")

async def on_shutdown(bot: Bot, admin_ids: list[int]):
    await bot.delete_webhook()
    await broadcaster.broadcast(bot, admin_ids, "Бот остановлен")


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    middleware_types = [
        ConfigMiddleware(config),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)

def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")

def get_storage(config):
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()

async def main():
    setup_logging()
    
    # Load config
    config = load_config(".env")
    storage = get_storage(config)

    # Initialize bot and dispatcher
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    # Include routers
    dp.include_routers(*routers_list)
    register_global_middlewares(dp, config)

    # Start webhook server
    await start_webhook_server(
        host="0.0.0.0",
        port=44123,
        bot=bot
    )
    
    # Notify admins
    await on_startup(bot, config.tg_bot.admin_ids)
    
    # Start bot polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        app = asyncio.run(main())
        web.run_app(app, host="127.0.0.1", port=PORT)
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
