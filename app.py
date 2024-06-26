import time
import os
import subprocess

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from datetime import date
import asyncio
from main import get_data, unzip
from src.schemas import StartEmulation
from src.exceptions import ArchiveAlreadyDownloaded


app = FastAPI()
#start_date = "2019-06-23"
#stations = ['ABPO00MDG', 'ALBH00CAN', 'ALGO00CAN', 'ALIC00AUS', 'AREG00PER']
start_date = None
stations = []


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
                    if 'station' not in line:
                        await websocket.send_text(line)
            await asyncio.sleep(1)  # Пауза перед следующим чтением файла
    except Exception as e:
        await websocket.close()
        print(f"WebSocket closed with exception: {e}")

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
        print("Call /start to set date")

    return {"date": start_date}


@app.get("/show_stations")
async def show_stations():
    stations = get_all_stations()
    return {"stations": stations}


@app.get("/get_stations")
async def get_stations():
    if stations is None:
        print("List of stations hasn't been set. Do it using /start")

    return {"stations": stations}


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


@app.post("/start")
async def start_emulation(data: StartEmulation):
    """
    Gets date of start emulation. Then prepare RINEX files with data and start system daemons
    for emulating publishing data from files.
    """

    global start_date

    start_date = data.start_date.strftime("%Y-%m-%d")
    
    try:
        print("Getting data in /start")
        await get_data(start_date)
        print("Data is gotten")

        print("Unpacking zip")
        await unzip(start_date)
        print("Archive has been unpacked")
    except ArchiveAlreadyDownloaded:
        print(f"Can't download archive for {start_date} becouse it's already downloaded")

    print("Call check_stations()")
    check_stations(data.stations)
    if len(stations) == 0:
        raise HTTPException(status_code=404,
                            detail="Of the transmitted stations, there are none that were on the transmitted date")

    str_stations = " ".join(stations)

    print("Removing all old services")
    subprocess.call("./scripts/for_tests/remove_services.sh", shell=True)

    print("Generating services' generator")
    subprocess.call(f"./scripts/services_generator.sh {str_stations}", shell=True)

    print(data.start_date)
    print(data.stations)

    subprocess.call(f"./scripts/run_subscriber.sh", shell=True)
    
    return {'status': 'okay'}
