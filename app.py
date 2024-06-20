from fastapi import FastAPI
from datetime import date


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello on root of Satellite Emulator app"}


@app.post("/start")
async def start_emulation(date: date):
    """
    Gets date of start emulation. Then prepare RINEX files with data and start system daemons
    for emulating publishing data from files.
    """
    pass

