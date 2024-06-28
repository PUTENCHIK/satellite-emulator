import os
import subprocess
import sys
import requests
import datetime
from src.exceptions import (
    ArchiveAlreadyDownloaded, DateIsTooLate, NoDataInStorage, IncorrectDate
)
from src.config import settings


async def get_data(date: str):
    from app import path
    try:
        gotten_date = datetime.date.fromisoformat(date)
    except ValueError:
        raise IncorrectDate(date)

    if gotten_date > datetime.date.today() - datetime.timedelta(days=1):
        raise DateIsTooLate(gotten_date)

    conf = settings()
    app_port = conf['app_port']
        
    #response = requests.get(f"127.0.0.1:{app_port}/get_path")
    #path = response.json()['path']

    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"archives/{date}.zip"

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
    subprocess.call(f"./scripts/prepare_files.sh {date}", shell=True)


async def check_stations(arr: list):
    from app import get_all_stations
    stations = []
    conf = settings()
    app_port = conf['app_port']
    
    directories_dict = await get_all_stations()
    directories = directories_dict['stations']
    """
    response = requests.get(f"http://127.0.0.1:{app_port}/get_all_stations")
    directories = response.json()['stations']
    """

    for station in arr:
        if station in directories:
            stations += [station]
    return stations


async def try_download(dt: str, i = 1) -> dict:
    if i > 5:
        return {'status': False, 'ex': None}

    try:
        await get_data(dt)
        return {'status': True, 'ex': None}
    except (ArchiveAlreadyDownloaded, DateIsTooLate, NoDataInStorage, IncorrectDate) as ex:
        return {'status': False, 'ex': ex}
    except Exception as ex:
        return await try_download(dt, i+1)

