import os
from urllib import response

import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()
load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")

BASE_URL = "https://platform-api2.max.ru"


def main():
    print("Ждём события MAX...")

    response = requests.get(
        f"{BASE_URL}/updates",
        headers={
            "Authorization": MAX_BOT_TOKEN
        },
        params={
            "limit": 100,
            "timeout": 60,
            "types": "message_created"
        }
    )

    print(f"HTTP: {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    main()
    print(f"HTTP: {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    main()