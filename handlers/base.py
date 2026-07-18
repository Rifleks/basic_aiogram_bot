from aiogram import F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline import start_keyboard

# ==========================================
# TEXTS
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

# ==========================================
# HANDLERS (COMMANDS & CALLBACKS)
# ==========================================

# Handle /start command using specific CommandStart filter
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
async def cmd_help(message: Message) -> None:
    await message.answer(get_help_text())

# Handle callback query from inline button using Magic Filter (F.data)
async def cq_get_commands_list(callback: types.CallbackQuery) -> None:
    # Answer the message where the button was clicked
    await callback.message.answer(get_help_text())
    # Always answer callback queries to stop the loading spinner in Telegram client
    await callback.answer()

def register_handlers(dp):
    """Register all base handlers."""
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_help, Command("help"))
    dp.callback_query.register(cq_get_commands_list, F.data == "get_commands_list")