import os
import json
import asyncio
import logging

from telethon import TelegramClient

from config import *
from max_sender import send_post
import time




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


DOWNLOAD_STATE_FILE = "downloads_state.json"


LOCK_FILE = "sync.lock"

LOCK_TIMEOUT = 2 * 60 * 60  # 2 часа


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

# ---------------- STATE MAX ----------------

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



# ---------------- STATE DOWNLOADS ----------------

def load_download_state():

    if not os.path.exists(DOWNLOAD_STATE_FILE):
        return {}


    with open(
        DOWNLOAD_STATE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_download_state(post_id, file_path):

    state = load_download_state()

    state[str(post_id)] = file_path


    with open(
        DOWNLOAD_STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            state,
            f,
            indent=4,
            ensure_ascii=False
        )



# ---------------- TELEGRAM ----------------

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



async def download_media(message):

    os.makedirs(
        DOWNLOAD_DIR,
        exist_ok=True
    )


    # ищем уже скачанный файл этого поста

    prefix = f"telegram_{message.id}_"


    for filename in os.listdir(DOWNLOAD_DIR):

        if filename.startswith(prefix):

            existing = os.path.join(
                DOWNLOAD_DIR,
                filename
            )

            print("Файл уже существует:")
            print(existing)

            return existing



    print("Скачиваем медиа...")


    temp_file = await message.download_media(
        file=DOWNLOAD_DIR
    )


    if not temp_file:
        return None


    # новое имя с Telegram ID

    ext = os.path.splitext(temp_file)[1]


    new_file = os.path.join(
        DOWNLOAD_DIR,
        f"telegram_{message.id}_{os.path.basename(temp_file)}"
    )


    os.rename(
        temp_file,
        new_file
    )


    print("Файл сохранён:")
    print(new_file)


    return new_file



# ---------------- MAIN ----------------

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



    file_path = None


    if message.media:

        file_path = await download_media(
            message
        )


        print(
            file_path
        )



    success = False



    if file_path:

        success = send_post(
            message.text or "",
            file_path
        )


    else:

        print(
            "Пост без медиа пока пропускаем"
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



if __name__ == "__main__":


    if not create_lock():

        exit()


    try:

        asyncio.run(main())


    finally:

        remove_lock()