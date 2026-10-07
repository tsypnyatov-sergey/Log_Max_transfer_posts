import os
import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()
load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")

BASE_URL = "https://platform-api2.max.ru"


def main():
    print("Получаем список чатов MAX...")

    response = requests.get(
        f"{BASE_URL}/chats",
        headers={
            "Authorization": MAX_BOT_TOKEN
        },
        params={
            "count": 100
        }
    )

    print(f"HTTP: {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    main()