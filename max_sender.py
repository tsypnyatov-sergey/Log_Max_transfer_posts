import os
import re
import requests
import urllib3

from config import MAX_BOT_TOKEN, MAX_CHANNEL_ID


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


MAX_API = "https://platform-api2.max.ru"


def upload_media(file_path, media_type):

    print(
        f"1. Получаем URL загрузки MAX ({media_type})..."
    )


    r = requests.post(
        f"{MAX_API}/uploads?type={media_type}",
        headers={
            "Authorization": MAX_BOT_TOKEN
        },
        verify=False,
        timeout=60
    )


    print(
        "HTTP:",
        r.status_code
    )


    if r.status_code != 200:

        print(r.text)

        return None



    data = r.json()


    print(data)



    upload_url = data.get("url")

    token = data.get("token")



    if not upload_url:

        print(
            "Нет URL загрузки"
        )

        return None



    print(
        "URL загрузки получен"
    )



    print(
        "2. Загружаем файл..."
    )



    try:

        with open(file_path, "rb") as f:


            upload_response = requests.post(

                upload_url,

                files={
                    "file": (
                        os.path.basename(file_path),
                        f
                    )
                },

                verify=False,

                timeout=300

            )


    except Exception as e:

        print(
            "Ошибка загрузки:"
        )

        print(e)

        return None




    print(
        "HTTP:",
        upload_response.status_code
    )


    print(
        upload_response.text
    )



    if upload_response.status_code != 200:

        return None




    media_id = None

    # Видео
    match = re.search(
        r"<retval>(\d+)</retval>",
        upload_response.text
    )

    if match:
        media_id = match.group(1)

        print(
            "Видео ID:",
            media_id
        )

        return {
            "token": token,
            "id": media_id
        }

    # Фото
    try:

        response_json = upload_response.json()

        photos = response_json.get("photos")

        if photos:
            photo_token = photos["0"]["token"]

            print(
                "Фото token получен"
            )

            return {
                "token": photo_token
            }


    except Exception as e:

        print(
            "Ошибка обработки фото:",
            e
        )

    print(
        "Не удалось получить данные медиа"
    )

    return None




def send_post(text, file_path=None):


    body = {

        "text": text

    }



    if file_path:


        ext = os.path.splitext(
            file_path
        )[1].lower()



        if ext in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        ]:

            media_type = "image"

            attachment_type = "image"



        elif ext in [
            ".mp4",
            ".mov",
            ".avi"
        ]:

            media_type = "video"

            attachment_type = "video"



        else:

            print(
                "Неизвестный файл:",
                ext
            )

            return False




        media = upload_media(
            file_path,
            media_type
        )


        if not media:

            return False



        body["attachments"] = [

            {

                "type": attachment_type,

                "payload": media

            }

        ]





    print(
        "3. Публикуем пост в MAX..."
    )



    r = requests.post(

        f"{MAX_API}/messages",

        headers={

            "Authorization": MAX_BOT_TOKEN,

            "Content-Type": "application/json"

        },

        params={

            "chat_id": MAX_CHANNEL_ID

        },

        json=body,

        verify=False,

        timeout=60

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