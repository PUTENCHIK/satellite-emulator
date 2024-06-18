import subprocess
import sys
import requests
import datetime


date = "2023-11-06"
TIME_INTERVAL = 600         #in sec


def get_data(date: str):
    try:
        gotten_date = datetime.date.fromisoformat(date)
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    if gotten_date > datetime.date.today() - datetime.timedelta(days=1):
        raise Exception(f"Gotten date must be early then today")

    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"archives/{date}.zip"
    with open(file_name, "wb") as f:
        print(f"Downloading {file_name}")
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if response.json()['detail'] == "Map files not foud":
            raise Exception(f"Sorry but storage doesn't save archive for date {date}")

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


def unzip(date: str):
    print("unzip func")
    subprocess.call(f"./script.sh {date}", shell=True)


def separate_files(date: str):
    subprocess.call(f"./scripts/create_interval_folders.sh {TIME_INTERVAL}", shell=True)


get_data(date)
unzip(date)

