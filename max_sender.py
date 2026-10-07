import os
import re
import requests
import urllib3

from config import MAX_BOT_TOKEN, MAX_CHANNEL_ID


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


MAX_API = "https://platform-api2.max.ru"


def upload_video(video_path):

    print("1. Получаем URL загрузки MAX...")


    r = requests.post(
        f"{MAX_API}/uploads?type=video",
        headers={
            "Authorization": MAX_BOT_TOKEN
        },
        verify=False
    )


    print("HTTP:", r.status_code)


    if r.status_code != 200:
        print(r.text)
        return None


    data = r.json()


    upload_url = data["url"]
    token = data["token"]


    print("Токен видео получен")


    print("2. Загружаем файл...")


    with open(video_path, "rb") as f:

        upload_response = requests.post(
            upload_url,
            files={
                "file": (
                    os.path.basename(video_path),
                    f,
                    "video/mp4"
                )
            },
            verify=False
        )


    print(
        "HTTP:",
        upload_response.status_code
    )


    print(
        upload_response.text
    )


    if upload_response.status_code != 200:
        print("Ошибка загрузки видео")
        return None


    match = re.search(
        r"<retval>(\d+)</retval>",
        upload_response.text
    )


    if not match:
        print("Не найден ID видео")
        return None


    video_id = match.group(1)


    print(
        "Видео ID:",
        video_id
    )


    return {
        "token": token,
        "id": video_id
    }



def send_post(text, video_path=None):


    body = {
        "text": text
    }


    if video_path:


        video = upload_video(video_path)


        if not video:
            return False


        body["attachments"] = [
            {
                "type": "video",
                "payload": video
            }
        ]


    print("3. Публикуем пост в MAX...")


    r = requests.post(
        f"{MAX_API}/messages",
        headers={
            "Authorization": MAX_BOT_TOKEN,
            "Content-Type": "application/json"
        },
        json=body,
        params={
            "chat_id": MAX_CHANNEL_ID
        },
        verify=False
    )


    print(
        "HTTP:",
        r.status_code
    )


    print(
        r.text
    )


    if r.status_code == 200:

        print(
            "Пост опубликован"
        )

        return True


    print(
        "Ошибка публикации MAX"
    )

    return False