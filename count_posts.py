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
    await client.start()

    total = 0
    first_id = None
    last_id = None

    async for message in client.iter_messages(
        CHANNEL,
        reverse=True
    ):
        if not message.text and not message.media:
            continue

        total += 1

        if first_id is None:
            first_id = message.id

        last_id = message.id

    print()
    print("Всего нормальных постов:", total)
    print("Первый пост ID:", first_id)
    print("Последний пост ID:", last_id)


if __name__ == "__main__":
    asyncio.run(main())