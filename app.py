import os
import subprocess

from fastapi import FastAPI
from datetime import date


app = FastAPI()
#date = None
start_date = "2019-06-23"
stations = ['ABPO00MDG', 'ALBH00CAN', 'ALGO00CAN', 'ALIC00AUS', 'AREG00PER']


@app.get("/")
async def root():
    return {"message": "Hello on root of Satellite Emulator app"}


@app.get("/get_date")
async def get_date():
    if start_date is None:
        print("Call /start to set date")
    return start_date


@app.get("/get_stations")
async def get_stations():
    return {
            'stations': stations
    }


@app.post("/start")
async def start_emulation(start_date: date):
    """
    Gets date of start emulation. Then prepare RINEX files with data and start system daemons
    for emulating publishing data from files.
    """

#    os.system("src/subscriber.py")
#    subprocess.run(["python", "src/subscriber.py"])
    subprocess.call(f"./scripts/run_subscriber.sh")
    
    return {'status': 'okay'}
    # Преобразуем дату в строковый формат YYYY-MM-DD
#    date_str = date.isoformat()

    # Запуск main.py с помощью subprocess
 #   subprocess.run(["python", "main.py", date_str])

    # Оставшаяся логика:
    # 1. Вызов get_data(date_str) из второго файла
    # 2. Вызов unzip(date_str) из второго файла
    # 3. Вызов separate_files(date_str) из второго файла
    # 4. Запуск демонов (пока в примере не реализовано)

#    return {"message": f"Emulation started for date {date_str}"}


#if __name__ == "__main__":
