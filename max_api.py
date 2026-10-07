import os
import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()
load_dotenv()

MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
MAX_CHANNEL_ID = os.getenv("MAX_CHANNEL_ID")

BASE_URL = "https://platform-api2.max.ru"


def upload_video(file_path):
    print("Загрузка видео в MAX...")

    response = requests.post(
        f"{BASE_URL}/uploads",
        params={"type": "video"},
        headers={
            "Authorization": MAX_BOT_TOKEN,
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Ошибка получения upload URL: {response.text}"
        )

    data = response.json()

    upload_url = data["url"]
    token = data["token"]

    with open(file_path, "rb") as video:
        upload_response = requests.post(
            upload_url,
            files={
                "data": (
                    os.path.basename(file_path),
                    video,
                    "video/mp4",
                )
            },
        )

    if upload_response.status_code != 200:
        raise Exception(
            f"Ошибка загрузки видео: {upload_response.text}"
        )

    print("Видео загружено в MAX")

    return token


def send_video(text, video_token):
    print("Публикация поста в MAX...")

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
            "text": text,
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

    if response.status_code != 200:
        raise Exception(
            f"Ошибка публикации MAX: {response.text}"
        )

    print("Пост опубликован в MAX")

    return response.json()