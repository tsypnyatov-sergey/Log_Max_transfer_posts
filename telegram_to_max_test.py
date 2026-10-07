import os
import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()
load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_CHANNEL_ID = os.getenv("MAX_CHANNEL_ID")

BASE_URL = "https://platform-api2.max.ru"

VIDEO_FILE = r"downloads\document_2025-10-15_14-05-52.mp4"

TEXT = """
Работать надо головой, а ещё лучше головой #LogMax🌲🌲🌲🤟
""".strip()


def upload_video():
    print("1. Получаем URL загрузки MAX...")

    response = requests.post(
        f"{BASE_URL}/uploads",
        params={"type": "video"},
        headers={
            "Authorization": MAX_BOT_TOKEN,
        },
    )

    print("HTTP:", response.status_code)

    data = response.json()

    upload_url = data["url"]
    token = data["token"]

    print("Токен видео получен")

    print("2. Загружаем файл...")

    with open(VIDEO_FILE, "rb") as f:
        upload = requests.post(
            upload_url,
            files={
                "data": (
                    os.path.basename(VIDEO_FILE),
                    f,
                    "video/mp4",
                )
            },
        )

    print("HTTP:", upload.status_code)
    print(upload.text)

    return token


def send_message(video_token):
    print("3. Отправляем пост в MAX...")

    response = requests.post(
        f"{BASE_URL}/messages",
        params={
            "chat_id": MAX_CHANNEL_ID
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
        }
    )

    print("HTTP:", response.status_code)
    print(response.text)


def main():
    if not os.path.exists(VIDEO_FILE):
        print("Нет файла:", VIDEO_FILE)
        return

    token = upload_video()

    send_message(token)


if __name__ == "__main__":
    main()