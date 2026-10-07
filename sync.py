import os
import json
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from max_api import upload_video, send_video
import logging
from datetime import datetime

logging.basicConfig(
    filename="logs/sync.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

STATE_FILE = "sync_state.json"
DOWNLOAD_DIR = "downloads"

client = TelegramClient(
    "logmax_session",
    API_ID,
    API_HASH
)


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_post_id": 0}

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(last_post_id):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"last_post_id": last_post_id},
            f,
            ensure_ascii=False,
            indent=4
        )


async def find_next_post(last_post_id):
    async for message in client.iter_messages(
        CHANNEL,
        reverse=True
    ):
        # Берём только сообщения после последнего обработанного
        if message.id <= last_post_id:
            continue

        # Пропускаем пустые служебные сообщения
        if not message.text and not message.media:
            continue

        return message

    return None


async def main():
    print("Подключаемся к Telegram...")
    await client.start()

    state = load_state()
    last_post_id = state["last_post_id"]

    print(f"Последний обработанный пост: {last_post_id}")

    message = await find_next_post(last_post_id)

    if not message:
        print("Новых постов для переноса нет.")
        return

    print("\n--- СЛЕДУЮЩИЙ ПОСТ ---")
    print(f"ID: {message.id}")
    print(f"Дата: {message.date}")
    print(f"Текст:\n{message.text or '[без текста]'}")

    if message.media:
        print("\nМедиа найдено.")
        print(f"Тип: {type(message.media).__name__}")

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        file_path = await message.download_media(
            file=DOWNLOAD_DIR
        )

        print(f"Медиа сохранено: {file_path}")
    else:
        print("\nМедиа нет.")

    # Отправляем в MAX только после скачивания

    if message.media:
        video_token = upload_video(file_path)

        send_video(
            message.text or "",
            video_token
        )

    else:
        print("Текстовый пост без медиа пока не отправляем")

    # Только после успешной публикации MAX
    save_state(message.id)

    print(
        f"\nСостояние сохранено: последний пост = {message.id}"
    )


if __name__ == "__main__":
    asyncio.run(main())