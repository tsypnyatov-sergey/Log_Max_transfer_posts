import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

client = TelegramClient(
    "logmax_session",
    API_ID,
    API_HASH
)

DOWNLOAD_DIR = "downloads"


async def main():
    print("Подключаемся к Telegram...")
    await client.start()

    print("Получаем пост ID 4...")

    message = await client.get_messages(
        CHANNEL,
        ids=4
    )

    if not message:
        print("Пост ID 4 не найден.")
        return

    print("\n--- ПОСТ ---")
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

        print(f"Медиа сохранено:")
        print(file_path)
    else:
        print("\nМедиа отсутствует.")


if __name__ == "__main__":
    asyncio.run(main())