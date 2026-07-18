# 🤖 The Ultimate Beginner's Guide to Telegram Bots (aiogram 3.x)

Welcome! If you are just starting your journey into Python and Telegram bot development, you have landed in the right place. 

This repository is designed to be a modern, and starter template using **aiogram 3**. We will walk you through everything from setting up your development environment to understanding real-world code architecture.

---

## 📖 Table of Contents
1. [What Will You Learn Here?](#-what-will-you-learn-here)
2. [Prerequisites & Setting Up](#-prerequisites--setting-up)
3. [Getting Your Bot Token from BotFather](#-getting-your-bot-token-from-botfather)
4. [Project Setup & Installation](#-project-setup--installation)
5. [Architecture: Single-File vs. Modular](#-architecture-single-file-vs-modular)
   - [The Single-File Prototype (`bot.py`)](#1-the-single-file-prototype-botpy)
   - [The Modular Architecture (Recommended)](#2-the-modular-architecture-recommended)
6. [Key Concepts Explained for Beginners](#-key-concepts-explained-for-beginners)
   - [What is Long Polling vs. Webhooks?](#what-is-long-polling-vs-webhooks)
   - [Magic Filters (`F`)](#magic-filters-f)
   - [Why Handler Order Matters!](#why-handler-order-matters)
7. [How to Run the Bot](#-how-to-run-the-bot)
8. [Useful Resources](#-useful-resources)

---

## 💡 What Will You Learn Here?

This project is packed with practical, real-world examples:
- **Command Handling:** How to neatly process `/start` and `/help` commands.
- **Dynamic Keyboards:** Building inline buttons with callback data and direct URL links.
- **Modern Callbacks:** Responding to button clicks without writing clumsy lambda functions, utilizing modern Magic Filters (`F.data`).
- **Media & Stickers:** Sending stickers by their unique ID and reading metadata (like file IDs and sizes) from stickers sent by users.
- **Safe Fallbacks:** Catching arbitrary, unexpected messages without crashing your application.
- **Security Best Practices:** Safely loading API tokens from environment variables (`.env`) so you never accidentally leak sensitive secrets on GitHub.

---

## 🛠 Prerequisites & Setting Up

Before running the code, make sure you have:
1. **Python 3.8 or higher** installed on your computer. You can check your version in the terminal/command prompt:
   ```bash
   python --version
   ```
2. A basic understanding of how to run commands in your terminal or IDE (like VS Code or PyCharm).

---

## 🤖 Getting Your Bot Token from BotFather

Every Telegram bot needs a unique secret key called a **Token** to communicate with Telegram's servers.
1. Open Telegram and search for **[@BotFather](https://t.me/BotFather)** (make sure it has the official blue checkmark).
2. Start a chat and send the command `/newbot`.
3. Follow the instructions:
   - Give your bot a **display name** (e.g., `My Awesome Bot`).
   - Give your bot a **username** (must end in `bot`, e.g., `my_awesome_test_bot`).
4. BotFather will give you a long string that looks like this:
   `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
5. **Copy this token!** Keep it secret and never share it publicly.

---

## 📦 Project Setup & Installation

### 1. Clone or Download the Repository
```bash
git clone https://github.com/Rifleks/basic_aiogram_bot.git
cd basic_aiogram_bot
```

### 2. Create a Virtual Environment
A virtual environment isolates your project dependencies so they do not interfere with other Python projects on your computer.

```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate
```
*(When activated, you should see `(venv)` appear at the start of your terminal command line).*

### 3. Install the Required Libraries
We use `requirements.txt` to install all necessary packages (`aiogram` and `python-dotenv`):
```bash
pip install -r requirements.txt
```

### 4. Configure Your Environment Variables
Never paste your bot token directly into your Python code! If you upload it to GitHub, bots can steal it within seconds.
1. Locate the file named `.env.example` in the project root.
2. Rename it to `.env` (or copy it and name the copy `.env`).
3. Open `.env` in a text editor and paste the token you got from BotFather:
   ```env
   BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

---

## 🗺 Architecture: Single-File vs. Modular

When learning, it is natural to put everything into a single script. But as your project expands, managing thousands of lines in one file becomes impossible. This repository demonstrates both approaches so you can transition smoothly!

### 1. The Single-File Prototype (`bot.py`)
If you want to quickly test an idea or understand the bare-bones flow of an asynchronous Telegram bot, check out `bot.py`. It contains the Dispatcher, handlers, and keyboard layouts all in one place.

### 2. The Modular Architecture (Recommended)
In professional development, we organize code by responsibility using **Routers**. Think of a Router as a mini-dispatcher that manages a specific feature of your bot.

```text
my_aiogram_bot/
│
├── handlers/            # Where your bot's logic lives
│   ├── __init__.py
│   ├── base.py          # Basic commands (/start, /help) & menu callbacks
│   └── media.py         # Sticker handling & fallback catch-all messages
│
├── keyboards/           # UI elements
│   ├── __init__.py
│   └── inline.py        # Functions that build buttons and menus
│
├── config.py            # Loads and validates variables from .env
├── main.py              # The entry point: registers routers and starts the bot
├── .env.example         # Template for required environment variables
├── .gitignore           # Tells Git to ignore sensitive files (like .env!)
└── requirements.txt     # List of project dependencies
```

---

## 🧠 Key Concepts Explained for Beginners

### What is Long Polling vs. Webhooks?
In this guide, we use **Long Polling** (`dp.start_polling(bot)`). This means your script constantly asks Telegram: *"Are there any new messages?"* It is perfect for beginners because it works right out of the box on your local computer without needing public IP addresses, domain names, or SSL certificates (which are required for Webhooks).

### Magic Filters (`F`)
In older bot libraries, checking message types or button clicks required writing repetitive `lambda` functions. aiogram 3 introduces **Magic Filters** (`F`). For example:
- `F.data == "get_commands_list"` cleanly checks if a clicked button has that specific callback data.
- `F.sticker` checks if the incoming message contains a sticker.
This makes your code much easier to read and maintain!

### Why Handler Order Matters!
In aiogram, messages are checked against handlers **from top to bottom** in the exact order they were registered. 

In our modular setup, look at `main.py`:
```python
dp.include_router(base.router)
dp.include_router(media.router)
```
Why is `base.router` included first? Because inside `media.py`, we have a fallback handler (`@router.message()`) that catches **any** message that hasn't been handled yet. If we included `media.router` first, that fallback handler would intercept everything, and your `/start` and `/help` commands in `base.py` would never get triggered!

---

## 🚀 How to Run the Bot

Once you have installed dependencies and set up your `.env` file, simply run:

```bash
python main.py
```
*(Or run `python bot.py` if you are experimenting with the single-file prototype).*

In your terminal, you will see logging output indicating that the bot has successfully started. Now, open Telegram, find your bot, send `/start`, and enjoy! 🎉

---

## 📚 Useful Resources

- [Official aiogram 3 Documentation](https://docs.aiogram.dev/) — The ultimate reference for advanced features like Finite State Machines (FSM), middlewares, and custom filters.
- [Telegram Bot API Official Reference](https://core.telegram.org/bots/api) — Complete documentation of all objects, methods, and data types provided by Telegram.
- [Python Asyncio Documentation](https://docs.python.org/3/library/asyncio.html) — To better understand asynchronous programming in Python.

---

## 🤝 Contributing & Feedback

Did you find a typo, or do you have an idea for another beginner-friendly example? Feel free to open an Issue or submit a Pull Request. Happy coding!