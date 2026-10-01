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


async def main():
    print("Подключаемся к Telegram...")

    await client.start()

    print("Telegram подключен.")

    me = await client.get_me()
    print(f"Авторизован как: {me.first_name}")

    print(f"Открываем канал: {CHANNEL}")

    messages = await client.get_messages(CHANNEL, limit=1)

    if not messages:
        print("Постов не найдено.")
        return

    message = messages[0]

    print("\n--- ПОСЛЕДНИЙ ПОСТ ---")
    print(f"ID: {message.id}")
    print(f"Дата: {message.date}")
    print(f"Текст:\n{message.text}")

    if message.media:
        print("\nУ поста есть медиафайл.")


if __name__ == "__main__":
    asyncio.run(main())