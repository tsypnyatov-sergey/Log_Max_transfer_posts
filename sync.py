import os
import json
import asyncio
import logging
import time

from telethon import TelegramClient

from config import *
from max_sender import send_post


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


LOCK_FILE = "sync.lock"

LOCK_TIMEOUT = 2 * 60 * 60  # 2 часа



# ================= LOCK =================

def create_lock():

    if os.path.exists(LOCK_FILE):

        file_age = time.time() - os.path.getmtime(LOCK_FILE)


        if file_age < LOCK_TIMEOUT:

            print(
                "Синхронизация уже запущена. Выход."
            )

            return False


        else:

            print(
                "Старый lock найден. Удаляем."
            )

            os.remove(LOCK_FILE)



    with open(
        LOCK_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            str(os.getpid())
        )


    return True



def remove_lock():

    if os.path.exists(LOCK_FILE):

        os.remove(LOCK_FILE)



# ================= STATE =================

def load_state():

    if not os.path.exists(STATE_FILE):

        return 0


    with open(
        STATE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)["last_post_id"]



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



# ================= TELEGRAM =================

async def find_next_post(last_id):

    async for message in client.iter_messages(
        TELEGRAM_CHANNEL,
        reverse=True
    ):

        if message.id <= last_id:
            continue


        if not message.text and not message.media:
            continue


        return message


    return None



# ================= DOWNLOAD =================

async def download_media(message):

    os.makedirs(
        DOWNLOAD_DIR,
        exist_ok=True
    )


    prefix = f"telegram_{message.id}_"


    # проверка существующего файла

    for filename in os.listdir(DOWNLOAD_DIR):

        if filename.startswith(prefix):

            existing = os.path.join(
                DOWNLOAD_DIR,
                filename
            )


            print(
                "Файл уже существует:"
            )

            print(existing)

            return existing



    print(
        "Скачиваем медиа..."
    )


    temp_file = await message.download_media(
        file=DOWNLOAD_DIR
    )


    if not temp_file:

        return None



    new_file = os.path.join(
        DOWNLOAD_DIR,
        f"telegram_{message.id}_{os.path.basename(temp_file)}"
    )



    if os.path.exists(new_file):

        os.remove(temp_file)


    else:

        os.rename(
            temp_file,
            new_file
        )



    print(
        "Файл сохранён:"
    )

    print(new_file)


    return new_file



# ================= MAIN =================

async def main():

    print(
        "Подключаемся к Telegram..."
    )


    await client.start()


    last_id = load_state()


    print(
        f"Последний обработанный пост: {last_id}"
    )


    message = await find_next_post(
        last_id
    )


    if not message:

        print(
            "Новых постов нет"
        )

        return



    print("====================")


    print(
        f"Telegram ID: {message.id}"
    )


    print(
        message.text or "[без текста]"
    )



    # если нет медиа

    if not message.media:

        print(
            "Пост без медиа. Пропускаем."
        )


        save_state(
            message.id
        )


        return



    file_path = await download_media(
        message
    )



    if not file_path:

        print(
            "Файл не получен"
        )

        return



    success = send_post(
        message.text or "",
        file_path
    )



    if success:


        save_state(
            message.id
        )


        logging.info(
            f"Telegram {message.id} -> MAX OK"
        )


        print(
            f"Состояние сохранено: {message.id}"
        )



    else:


        logging.error(
            f"Telegram {message.id} -> MAX ERROR"
        )


        print(
            "State НЕ изменён"
        )



# ================= START =================

if __name__ == "__main__":


    if not create_lock():

        exit()



    try:

        asyncio.run(main())


    finally:


        remove_lock()


        try:

            asyncio.run(
                client.disconnect()
            )

        except:

            pass