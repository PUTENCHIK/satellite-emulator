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
    # Преобразуем дату в строковый формат YYYY-MM-DD
    date_str = date.isoformat()

    # Запуск main.py с помощью subprocess
    subprocess.run(["python", "main.py", date_str])

    # Оставшаяся логика:
    # 1. Вызов get_data(date_str) из второго файла
    # 2. Вызов unzip(date_str) из второго файла
    # 3. Вызов separate_files(date_str) из второго файла
    # 4. Запуск демонов (пока в примере не реализовано)

    return {"message": f"Emulation started for date {date_str}"}
    pass

