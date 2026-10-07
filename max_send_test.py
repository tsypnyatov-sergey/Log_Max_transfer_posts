import os
import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()
load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_CHANNEL_ID = os.getenv("MAX_CHANNEL_ID")

BASE_URL = "https://platform-api2.max.ru"


def main():
    print("Отправляем тестовый пост в MAX...")

    response = requests.post(
        f"{BASE_URL}/messages",
        headers={
            "Authorization": MAX_BOT_TOKEN,
            "Content-Type": "application/json"
        },
        json={
            "text": "Тестовая публикация через API MAX"
        },
        params={
            "chat_id": MAX_CHANNEL_ID
        }
    )

    print(f"HTTP: {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    main()