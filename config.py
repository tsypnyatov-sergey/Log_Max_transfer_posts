import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL")


# MAX
MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_CHANNEL_ID = os.getenv("MAX_CHANNEL_ID")

# API адрес MAX
MAX_API = "https://platform-api2.max.ru"


# Files
STATE_FILE = "sync_state.json"
DOWNLOAD_STATE_FILE = "downloads_state.json"
DOWNLOAD_DIR = "downloads"
LOG_FILE = "logs/sync.log"