from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

# Handle /sticker command
async def cmd_sticker(message: Message) -> None:
    # Sending a specific sticker by its file_id
    await message.answer_sticker(
        sticker="CAACAgIAAxkBA1tINGpbqyRxutU8gE5SGRYuoHZ_vJEtAALYDwACSPJgSxX7xNp4dGuYPQQ"
    )

# Handle any incoming sticker from the user
async def handle_user_sticker(message: Message) -> None:
    await message.reply(
        f"🎉 Nice sticker!\n\n"
        f"<b>Sticker ID:</b> <code>{message.sticker.file_id}</code>\n"
        f"<b>File size:</b> {message.sticker.file_size or 0} bytes"
    )

# Fallback handler for any other text or content type (Must be at the very bottom!)
async def handle_any_message(message: Message) -> None:
    content_type = message.content_type
    await message.answer(
        f"You sent me a message of type: <code>{content_type}</code>\n"
        f"Use /help to see available commands."
    )

def register_handlers(dp):
    """Register all media handlers."""
    dp.message.register(cmd_sticker, Command("sticker"))
    dp.message.register(handle_user_sticker, F.sticker)
    dp.message.register(handle_any_message)  # Fallback - must be last