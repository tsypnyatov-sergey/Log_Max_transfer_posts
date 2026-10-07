import os
import json
import asyncio
import logging

from telethon import TelegramClient

from config import *
from max_sender import send_post


BATCH_SIZE = 10


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)


client = TelegramClient(
    "logmax_session",
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH
)



def load_state():

    if not os.path.exists(STATE_FILE):
        return 0

    with open(
        STATE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f).get(
            "last_post_id",
            0
        )



def save_state(post_id):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "last_post_id": post_id
            },
            f,
            indent=4
        )



async def get_posts(last_id):

    posts = []

    async for message in client.iter_messages(
        TELEGRAM_CHANNEL,
        reverse=True
    ):

        if message.id <= last_id:
            continue


        if not message.text and not message.media:
            continue


        posts.append(message)


        if len(posts) >= BATCH_SIZE:
            break


    return posts



async def download_media(message):

    os.makedirs(
        DOWNLOAD_DIR,
        exist_ok=True
    )


    prefix = f"telegram_{message.id}_"


    for filename in os.listdir(DOWNLOAD_DIR):

        if filename.startswith(prefix):

            path = os.path.join(
                DOWNLOAD_DIR,
                filename
            )

            print(
                "Файл уже существует:",
                path
            )

            return path



    print(
        "Скачиваем медиа..."
    )


    temp = await message.download_media(
        file=DOWNLOAD_DIR
    )


    if not temp:

        print(
            "Ошибка скачивания файла"
        )

        return None



    ext = os.path.splitext(temp)[1]


    new_file = os.path.join(
        DOWNLOAD_DIR,
        f"telegram_{message.id}{ext}"
    )


    if os.path.exists(new_file):

        os.remove(temp)

    else:

        os.rename(
            temp,
            new_file
        )


    print(
        "Файл:",
        new_file
    )


    return new_file



async def main():

    print(
        "Подключаемся к Telegram..."
    )


    await client.start()



    last_id = load_state()


    print(
        "Последний пост:",
        last_id
    )



    posts = await get_posts(
        last_id
    )



    if not posts:

        print(
            "Новых постов нет"
        )

        return



    count = 0



    for message in posts:


        print(
            "\n===================="
        )


        print(
            f"Telegram ID: {message.id}"
        )


        print(
            message.text or "[без текста]"
        )



        file_path = None



        try:


            if message.media:

                file_path = await download_media(
                    message
                )


            else:

                print(
                    "Текстовый пост без медиа"
                )



            print(
                "Отправляем в MAX..."
            )


            success = send_post(
                message.text or "",
                file_path
            )



            if success:


                save_state(
                    message.id
                )


                logging.info(
                    f"{message.id} -> MAX OK"
                )


                print(
                    "MAX OK"
                )


                count += 1


                await asyncio.sleep(10)



            else:


                logging.error(
                    f"{message.id} -> MAX ERROR"
                )


                print(
                    "Ошибка MAX. Остановка batch."
                )


                break



        except Exception as e:


            logging.exception(
                f"{message.id} -> EXCEPTION {e}"
            )


            print(
                "Ошибка:",
                e
            )


            print(
                "Остановка batch."
            )


            break




    print(
        f"\nГотово. Загружено: {count}"
    )



if __name__ == "__main__":

    asyncio.run(main())