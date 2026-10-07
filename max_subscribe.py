import os
import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()
load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")

BASE_URL = "https://platform-api2.max.ru"


def main():
    print("Создаём подписку MAX...")

    response = requests.post(
        f"{BASE_URL}/subscriptions",
        headers={
            "Authorization": MAX_BOT_TOKEN,
            "Content-Type": "application/json"
        },
        json={
            "update_types": [
                "message_created"
            ]
        }
    )

    print(f"HTTP: {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    main()