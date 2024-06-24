import os
import subprocess

from fastapi import FastAPI
from datetime import date


app = FastAPI()
start_date = "2019-06-23"
stations = ['ABPO00MDG', 'ALBH00CAN', 'ALGO00CAN', 'ALIC00AUS', 'AREG00PER']


@app.get("/")
async def root():
    return {"message": "Hello on root of Satellite Emulator app"}


@app.get("/get_date")
async def get_date():
    if start_date is None:
        print("Call /start to set date")

    return {"date": start_date}


@app.get("/get_stations")
async def get_stations():
    if stations is None:
        print("List of stations hasn't been set. Do it using /start")

    return {"stations": stations}


@app.get("/get_path")
async def get_path():
    return {"path": os.path.dirname(os.path.abspath(__file__))}


@app.post("/start")
async def start_emulation(start_date: date):
    """
    Gets date of start emulation. Then prepare RINEX files with data and start system daemons
    for emulating publishing data from files.
    """

    subprocess.call(f"./scripts/run_subscriber.sh")
    
    return {'status': 'okay'}
