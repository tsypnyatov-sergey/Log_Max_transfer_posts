import os
import requests
from dotenv import load_dotenv

load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_CHANNEL_ID = os.getenv("MAX_CHANNEL_ID")

BASE_URL = "https://platform-api2.max.ru"


def main():
    if not MAX_BOT_TOKEN:
        print("Ошибка: MAX_BOT_TOKEN не найден в .env")
        return

    if not MAX_CHANNEL_ID:
        print("Ошибка: MAX_CHANNEL_ID не найден в .env")
        return

    print("Проверяем подключение к MAX...")

    response = requests.get(
        f"{BASE_URL}/me",
        headers={
            "Authorization": MAX_BOT_TOKEN
        }
    )

    print(f"HTTP: {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    main()