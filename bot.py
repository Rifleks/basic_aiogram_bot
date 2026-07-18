import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set! Please check your .env file.")

# Configure logging to see bot actions in console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

# Initialize Dispatcher (root router)
dp = Dispatcher()


# ==========================================
# TEXTS & KEYBOARDS
# ==========================================
def get_help_text() -> str:
    """Returns the help message content."""
    return (
        "<b>🤖 Available Commands:</b>\n\n"
        "/start - Restart the bot & show greetings\n"
        "/help - Show this help message\n"
        "/sticker - Get a sample sticker\n\n"
        "<i>Tip: You can also send me any sticker or text!</i>"
    )


def start_keyboard() -> InlineKeyboardMarkup:
    """Builds the inline keyboard for the start command."""
    builder = InlineKeyboardBuilder()
    
    # Adding callback button and URL button
    builder.add(
        InlineKeyboardButton(text="📋 Commands list", callback_data="get_commands_list"),
        InlineKeyboardButton(text="📦 aiogram GitHub", url="https://github.com/aiogram/aiogram")
    )
    
    # Adjust layout: 1 button per row (vertical stack)
    builder.adjust(1)
    return builder.as_markup()


# ==========================================
# HANDLERS (COMMANDS & CALLBACKS)
# ==========================================

# Handle /start command using specific CommandStart filter
@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = message.from_user
    username_text = f"@{user.username}" if user.username else "No username"
    
    await message.answer(
        f"Hello, <b>{user.full_name}</b>!\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Username: {username_text}\n\n"
        "To see what I can do, use /help or <b>click the button below</b>:",
        reply_markup=start_keyboard()
    )


# Handle /help command
@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(get_help_text())


# Handle callback query from inline button using Magic Filter (F.data)
@dp.callback_query(F.data == "get_commands_list")
async def cq_get_commands_list(callback: types.CallbackQuery) -> None:
    # Answer the message where the button was clicked
    await callback.message.answer(get_help_text())
    # Always answer callback queries to stop the loading spinner in Telegram client
    await callback.answer()


# Handle /sticker command
@dp.message(Command("sticker"))
async def cmd_sticker(message: Message) -> None:
    # Sending a specific sticker by its file_id
    await message.answer_sticker(
        sticker="CAACAgIAAxkBA1tINGpbqyRxutU8gE5SGRYuoHZ_vJEtAALYDwACSPJgSxX7xNp4dGuYPQQ"
    )


# Handle any incoming sticker from the user
@dp.message(F.sticker)
async def handle_user_sticker(message: Message) -> None:
    await message.reply(
        f"🎉 Nice sticker!\n\n"
        f"<b>Sticker ID:</b> <code>{message.sticker.file_id}</code>\n"
        f"<b>File size:</b> {message.sticker.file_size or 0} bytes"
    )


# Fallback handler for any other text or content type (Must be at the very bottom!)
@dp.message()
async def handle_any_message(message: Message) -> None:
    content_type = message.content_type
    await message.answer(
        f"You sent me a message of type: <code>{content_type}</code>\n"
        f"Use /help to see available commands."
    )


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