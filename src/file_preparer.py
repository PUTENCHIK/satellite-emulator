import sys
import os
import requests
import schedule
import subprocess
import time
import asyncio
import datetime
#from datetime import datetime, timedelta, date

from models import Logger
from config import settings
from exceptions import (
    ArchiveAlreadyDownloaded, DateIsTooLate, NoDataInStorage, IncorrectDate
)


async def get_data(dt: str):
    log.add_debug(f"Date: {dt}")
    try:
        gotten_date = datetime.date.fromisoformat(dt)
    except ValueError:
        raise IncorrectDate(dt)

    if gotten_date > datetime.date.today() - datetime.timedelta(days=1):
        raise DateIsTooLate(gotten_date)

    link = f"https://api.simurg.space/datafiles/map_files?date={dt}"
    file_name = f"{path}/archives/{dt}.zip"

    print("Checking if archive exists")

    if os.path.exists(file_name):
        print("Getting headers")
        response = requests.head(link)
        total_length = response.headers.get('content-length')
        size = os.path.getsize(file_name)
        print(f"total_length: {total_length}, size: {size}")

        if size == total_length:
            print("ArchiveAlreadyDownloaded")
            raise ArchiveAlreadyDownloaded(file_name)
        else:
            os.remove(f"{path}/{file_name}")
            print("Removed old archive")

    with open(file_name, "wb") as f:
        print(f"Downloading {file_name}")
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if int(total_length) == 31:
            raise NoDataInStorage(date)

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()


async def unzip(date: str):
    print("unzip func")
    subprocess.call(f"../scripts/prepare_files.sh {date}", shell=True)


async def update_files():
    log.add_debug("Updating files")

    response = requests.get(f"http://127.0.0.1:{app_port}/get_date")
    start_date = response.json()['date']

    response = requests.get(f"http://127.0.0.1:{app_port}/get_all_stations")
    all_stations = response.json()['stations']

    log.add_debug(f"Gotten date from app: {start_date}")

    if start_date is None:
        log.add_debug("Can't update files for the next date because date is null")
    else:
        current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        # Trying to remove archive and files for previous date
        previous_date = current_date - datetime.timedelta(days=1)
        str_previous_date = previous_date.strftime("%Y-%m-%d")
        previous_archive = f"{path}/archives/{str_previous_date}.zip"
        if os.path.exists(previous_archive):
            log.add_debug(f"Removed old archive: {previous_archive}")
            os.remove(previous_archive)

        for station in all_stations:
            file_path = f"{path}/files/{station}/{str_previous_date}.rnx"
            if os.path.exists(file_path):
                log.add_debug(f"Removed old file: {file_path}")
                os.remove(file_path)

        # Trying to prepare files for the next date
        next_date = current_date + datetime.timedelta(days=1)
        str_next_date = next_date.strftime("%Y-%m-%d")
        
        log.add_debug(f"Trying to download archive and unpack it")
        result = await get_data(str_next_date)

        log.add_info("Unpacking zip")
        if result['status']:
            result['status'] = await unzip(str_next_date)
            log.add_info("Archive has been unpacked") 


def f_update():
    try:
        asyncio.run(update_files())
    except Exception as ex:
        log.add_warning(f"ex: {ex}")


if __name__ == "__main__":
    conf = settings()
    app_port = conf['app_port']

    response = requests.get(f"http://127.0.0.1:{app_port}/get_path")
    path = response.json()['path']

    log = Logger.Logger("file_preparer")

    schedule.every(6).hours.do(update_files)

    while True:
        schedule.run_pending()
        mins = 30
        time.sleep(mins*60)

