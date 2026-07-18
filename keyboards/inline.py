from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

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