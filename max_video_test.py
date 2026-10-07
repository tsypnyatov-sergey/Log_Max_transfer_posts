import os
import time
import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()
load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_CHANNEL_ID = os.getenv("MAX_CHANNEL_ID")

BASE_URL = "https://platform-api2.max.ru"

VIDEO_FILE = r"downloads\document_2025-10-15_14-05-52.mp4"
TEXT = "Работать надо головой, а ещё лучше головой #LogMax🌲🌲🌲🤟"


def main():
    if not os.path.exists(VIDEO_FILE):
        print(f"Файл не найден: {VIDEO_FILE}")
        return

    print("Шаг 1. Получаем URL для загрузки видео...")

    response = requests.post(
        f"{BASE_URL}/uploads",
        params={"type": "video"},
        headers={
            "Authorization": MAX_BOT_TOKEN,
            "Accept": "application/json",
        },
    )

    print(f"HTTP: {response.status_code}")
    print(response.text)

    if response.status_code != 200:
        return

    upload_data = response.json()

    upload_url = upload_data["url"]
    video_token = upload_data["token"]

    print("\nURL получен.")
    print(f"Токен получен: {video_token[:10]}...")

    print("\nШаг 2. Загружаем видео...")

    with open(VIDEO_FILE, "rb") as video:
        upload_response = requests.post(
            upload_url,
            headers={
                "Authorization": MAX_BOT_TOKEN,
            },
            files={
                "data": (
                    os.path.basename(VIDEO_FILE),
                    video,
                    "video/mp4",
                )
            },
        )

    print(f"HTTP: {upload_response.status_code}")
    print(upload_response.text)

    if upload_response.status_code != 200:
        return

    print("\nВидео загружено. Ждём обработки MAX...")
    time.sleep(5)

    print("\nШаг 3. Публикуем видео в канал...")

    message_response = requests.post(
        f"{BASE_URL}/messages",
        params={
            "chat_id": MAX_CHANNEL_ID,
        },
        headers={
            "Authorization": MAX_BOT_TOKEN,
            "Content-Type": "application/json",
        },
        json={
            "text": TEXT,
            "attachments": [
                {
                    "type": "video",
                    "payload": {
                        "token": video_token
                    }
                }
            ]
        },
    )

    print(f"HTTP: {message_response.status_code}")
    print(message_response.text)


if __name__ == "__main__":
    main()