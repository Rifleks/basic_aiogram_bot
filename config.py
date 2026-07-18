import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set! Please check your .env file.")