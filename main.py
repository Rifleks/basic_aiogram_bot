import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN
from handlers import register_all_handlers

# Configure logging to see bot actions in console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

# Initialize Dispatcher (root router)
dp = Dispatcher()

# Register all handlers
register_all_handlers(dp)

# ==========================================
# BOT ENTRY POINT
# ==========================================
async def main() -> None:
    # Initialize bot with HTML parse mode as default
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Retrieve and log bot details
    bot_info = await bot.get_me()
    logging.info(f"Starting bot: '{bot_info.full_name}' (@{bot_info.username}) [ID: {bot_info.id}]")

    # Drop pending updates to ignore messages sent while the bot was offline
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Start long-polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped by user.")