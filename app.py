import time
import os
import subprocess

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from datetime import datetime, date
import asyncio
from main import get_data, unzip
from src.schemas import StartEmulation, Stations
from src.exceptions import ArchiveAlreadyDownloaded
from src.models import Logger

app = FastAPI()
#start_date = "2019-06-23"
#stations = ['ABPO00MDG', 'ALBH00CAN', 'ALGO00CAN', 'ALIC00AUS', 'AREG00PER']
start_date = None
stations = []

log=Logger.Logger("App.py")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    file_path = "logs.log"
    try:
        # Получаем текущую длину файла при первом подключении
        with open(file_path, "r") as file:
            file.seek(0, os.SEEK_END)
            position = file.tell()

        while True:
            with open(file_path, "r") as file:
                file.seek(position)
                new_lines = file.readlines()
                position = file.tell()  # Обновляем позицию для следующего чтения
                for line in new_lines:
                    if 'subscriber' in line:
                        await websocket.send_text(line)
            await asyncio.sleep(1)  # Пауза перед следующим чтением файла
    except Exception as e:
        await websocket.close()
        log.add_error(f"WebSocket closed with exception: {e}")


@app.get("/")
async def get_root():
    # HTML и JavaScript код для открытия WebSocket соединения и отображения данных
    index_file= 'html/template.html'
    with open(index_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content)


@app.get("/get_date")
async def get_date():
    if start_date is None:
        log.add_info("Call /start to set date")

    return {"date": start_date}


@app.get("/show_stations")
async def show_stations() -> dict:
    """

    """
    stations = get_all_stations()
    arr = {}

    for station in stations:
        arr[station] = []
        for d in os.listdir(f"./files/{station}"):
            arr[station] += [d.split(".")[0]]

    return {"stations": arr}


@app.get("/get_stations")
async def get_stations():
    if stations is None:
        log.add_info("List of stations hasn't been set. Do it using /start")

    return {"stations": stations}


@app.get("/get_active_services")
async def get_active_services():
    stations = get_all_stations()
    arr = []

    for station in stations:
        service = f"{station}.service"

        try:
            result = subprocess.run(
                    ['systemctl', 'is-active', service],
                    capture_output=True, 
                    text=True, 
                    check=True
            )
            if result.returncode == 0:
                arr += [service]
        except Exception as ex:
            continue

    return {"active_services": arr}


def get_all_stations() -> list:
    stations = [d for d in os.listdir("./files/")]
    return stations


def check_stations(arr: list):
    global stations

    stations = []
    directories = get_all_stations()    
    for station in arr:
        if station in directories:
            stations += [station]
    

@app.get("/get_path")
async def get_path():
    return {"path": os.path.dirname(os.path.abspath(__file__))}


async def try_download(i = 1) -> bool:
    if i > 5:
        return False

    try:
        await get_data(start_date)
        return True
    except (ArchiveAlreadyDownloaded, DateIsTooLate, NoDataInStorage, IncorrectDate):
        return False
    except Exception as ex:
        return try_download(i+1)


@app.post("/start")
async def start_emulation(data: StartEmulation):
    """
    Gets date of start emulation. Then prepare RINEX files with data and start system daemons
    for emulating publishing data from files.
    """
    global start_date

    start_date = data.start_date.strftime("%Y-%m-%d")
    log.add_info("Getting data in /start")
    result = try_download()
    log.add_info("Data is gotten")
    log.add_info("Unpacking zip")
    await unzip(start_date)
    log.add_info("Archive has been unpacked")
    log.add_info("Call check_stations()")
    check_stations(data.stations)
    if len(stations) == 0:
        log.add_error("Of the transmitted stations, there are none that were on the transmitted date")
        raise HTTPException(status_code=404,
                            detail="Of the transmitted stations, there are none that were on the transmitted date")

    str_stations = " ".join(stations)
    log.add_info("Removing all old services")
    subprocess.call("./scripts/for_tests/remove_services.sh", shell=True)
    log.add_info("Generating services' generator")
    subprocess.call(f"./scripts/services_generator.sh {str_stations}", shell=True)

    print(data.start_date)
    print(data.stations)

    subprocess.call(f"./scripts/run_subscriber.sh", shell=True)
    
    return {'status': 'okay'}


@app.post("/stop")
async def stop_emulation(data: Stations):
    str_stations = " ".join(data.stations)
    log.add_info(f"Stop Stations {str_stations}")

    subprocess.call(f"./scripts/stop_services.sh {str_stations}", shell=True)
    return {"status": "stopped"}


@app.post("/restart")
async def restart_emulation(data: Stations):
    str_stations = " ".join(data.stations)
    log.add_info(f"Stop Stations {str_stations}")

    subprocess.call(f"./scripts/restart_services.sh {str_stations}", shell=True)
    return {"status": "restarted"}


@app.post("/update_date")
async def set_next_date():
    global start_date

    if datetime.now().time() > time(23, 59, 30):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=1)
        start_date = new_date.strftime("%Y-%m-%d") 
        log.add_info(f"Date was updated to {start_date} at {datetime.now()}")
        print(f"Date was updated to {start_date} at {datetime.now()}")
    else:
        print("Could be changed at least 23:59:30")
        log.add_info("Could be changed at least 23:59:30")
    return {"app_date": start_date}
