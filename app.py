import time
import os
import subprocess

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from datetime import datetime, date
import asyncio
from main import (get_data,
                  unzip,
                  check_stations,
                  try_download
)
from src.schemas import StartEmulation, Stations
from src.exceptions import (
    ArchiveAlreadyDownloaded, DateIsTooLate, NoDataInStorage, IncorrectDate
)
from src.models import Logger


app = FastAPI()
start_date = None
stations = []

log=Logger.Logger("App.py")
path = os.path.dirname(os.path.abspath(__file__))

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
                position = file.tell()
                for line in new_lines:
                    if 'subscriber' in line:
                        await websocket.send_text(line)
            await asyncio.sleep(1)
    except Exception as e:
        await websocket.close()
        log.add_error(f"WebSocket closed with exception: {e}")


@app.get("/")
async def get_root():
    index_file= 'html/template.html'
    with open(index_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
        return HTMLResponse(content=html_content)


@app.get("/get_date")
async def get_date():
    if start_date is None:
        log.add_info("Call /start to set date")

    return {"date": start_date}


@app.get("/get_all_stations")
async def get_all_stations():
    stations = [d for d in os.listdir("./files/")]
    return {'stations': stations}


@app.get("/show_stations")
async def show_stations() -> dict:
    stations_dict = await get_all_stations()
    stations = stations_dict['stations']
    arr = {}

    for station in stations:
        arr[station] = []
        for d in os.listdir(f"{path}/files/{station}"):
            arr[station] += [d.split(".")[0]]

    return {"stations": arr}


@app.get("/get_stations")
async def get_stations():
    if stations is None:
        log.add_info("List of stations hasn't been set. Do it using /start")

    return {"stations": stations}


@app.get("/get_active_services")
async def get_active_services():
    stations_dict = await get_all_stations()
    stations = stations_dict['stations']
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
    

@app.get("/get_path")
async def get_path():
    return {"path": path}


async def prepare_files(date: str):
    log.add_info("Trying to download archive")
    result = await try_download(start_date)

    log.add_info("Unpacking zip")
    if result['status']:
        result['status'] = await unzip(start_date)
        log.add_info("Archive has been unpacked")

    return result


@app.post("/start")
async def start_emulation(data: StartEmulation):
    """
    Gets date of start emulation. Then prepare RINEX files with data and start system daemons
    for emulating publishing data from files.
    """
    global start_date, stations, path

    start_date = data.start_date.strftime("%Y-%m-%d")

    result = prepare_files(start_date)

    log.add_info("Call check_stations()")
    if result['status'] or isinstance(result['ex'], ArchiveAlreadyDownloaded):
        stations = check_stations(data.stations)

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
    
        return {'success': True}
    else:
        return {'status': False, 'description': "Too late date or no data in storage for date"}


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
