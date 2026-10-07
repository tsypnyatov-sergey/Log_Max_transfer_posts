import os

import schedule
import time
import subprocess
import logging
from datetime import datetime

import sys


logging.basicConfig(
    filename="logs/scheduler.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

sys.stdout.reconfigure(
    encoding="utf-8"
)

def run_sync():

    logging.info("Запуск синхронизации Telegram -> MAX")

    try:

        result = subprocess.run(
            [
                ".venv\\Scripts\\python.exe",
                "sync.py"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={
                **os.environ,
                "PYTHONIOENCODING": "utf-8"
            }
        )


        logging.info(
            result.stdout
        )


        if result.stderr:

            logging.error(
                result.stderr
            )


    except Exception as e:

        logging.exception(e)



# расписание

schedule.every().day.at("08:00").do(run_sync)
schedule.every().day.at("12:00").do(run_sync)
schedule.every().day.at("17:00").do(run_sync)
schedule.every().day.at("20:00").do(run_sync)


logging.info(
    "Планировщик MAX запущен"
)


print(
    "Планировщик MAX запущен"
)


while True:

    schedule.run_pending()

    time.sleep(30)