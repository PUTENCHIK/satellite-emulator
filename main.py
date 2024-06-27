import os
import subprocess
import sys
import requests
import datetime
from src.exceptions import ArchiveAlreadyDownloaded, DateIsTooLate
from src.config import settings


async def get_data(date: str):
    try:
        gotten_date = datetime.date.fromisoformat(date)
    except ValueError:
        raise IncorrectDate(date)

    if gotten_date > datetime.date.today() - datetime.timedelta(days=1):
        raise DateIsTooLate(gotten_date)

    conf = settings()
    app_port = conf['app_port']
    response = requests.get(f"http://127.0.0.1:{app_port}/get_path")
    path = response.json()['path']

    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"archives/{date}.zip"

    if os.path.exists(file_name):
        response = requests.head(link)
        total_length = response.headers.get('content-length')
        size = os.path.getsize(file_name)

        if size == total_length:
            raise ArchiveAlreadyDownloaded(file_name)
        else:
            os.remove(f"{path}/file_name")
            print("Removed old archive")

    with open(file_name, "wb") as f:
        print(f"Downloading {file_name}")
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if response.json()['detail'] == "Map files not foud":
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

"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Неправильное количество аргументов. Используйте: python main.py YYYY-MM-DD")
        sys.exit(1)

    date = sys.argv[1]

    try:
        gotten_date = datetime.date.fromisoformat(date)
    except ValueError:
        print("Неправильный формат даты. Используйте YYYY-MM-DD")
        sys.exit(1)

    if gotten_date > datetime.date.today() - datetime.timedelta(days=1):
        print("Дата должна быть раньше или равна вчерашнему дню")
        sys.exit(1)

    get_data(date)
    unzip(date)
"""
