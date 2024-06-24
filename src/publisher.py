import sys
import os
import requests
import time
import schedule
import paho.mqtt.client as mqtt_client
from datetime import datetime, timedelta
from gnss_tec import rnx

from config import settings


def tec_to_string(tec) -> str:
    return '{} {}: {} {}'.format(
                tec.timestamp,
                tec.satellite,
                tec.phase_tec,
                tec.p_range_tec,
            )


def read_file(reader):
    global date

    arr = []
    phase = None
    for tec in reader:
        if len(arr) == 0:
            phase = tec.timestamp.second
#            arr += [tec_to_string(tec)]
            arr += [tec]
        else:
            i_phase = tec.timestamp.second
            if phase == i_phase:
#                arr += [tec_to_string(tec)]
                arr += [tec]
            else:
                yield arr
                arr = [tec]
                phase = i_phase
    yield arr


def rewrite_reader():
    global reader, date

    print("Changing date")

    new_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
    new_date = new_date.strftime("%Y-%m-%d")

    new_path = f"files/{station}/{new_date}.rnx"
    if os.path.exists(new_path):
        file = open(new_path)
        reader = rnx(file)
    else:
        print("File with new date doesn't exists")
        sys.exit(1)


if __name__ == "__main__":

    conf = settings()

    if len(sys.argv) != 2:
        raise Exception("Неправильное количество аргументов. Необходимо указать название станции")

    station = sys.argv[1]

    if not os.path.isdir(f"files/{station}"):
        raise Exception(f"Указанная станция не сущесвует: {station}")

    print("Getting date")
    app_port = conf['app_port']
    response = requests.get(f'http://127.0.0.1:{app_port}/get_date')
    date = response.json()
    print("Date:", date)

    file = open(f"files/{station}/{date}.rnx")
    reader = rnx(file)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1)
    client.connect("localhost", 1883, 60)
    client.loop_start()

    schedule.every().day.at("04:44:31").do(rewrite_reader)
    
    arr = read_file(reader)
    elem = next(arr)
    time_stamp = elem[0].timestamp
    custom_date = datetime(
            time_stamp.year,
            time_stamp.month,
            time_stamp.day,
            datetime.now().hour,
            datetime.now().minute,
            datetime.now().second
    )
        
    while True:
        row = elem[0]
        time_stamp = row.timestamp
        if time_stamp > custom_date:
            break
        else:
            try:
                elem = next(arr)
            except StopIteration:
                rewrite_reader()
                arr = read_file(reader)
                elem = next(arr)
                break
       

    while True:
        elem = ["{} {} {} {}".format(
            tec.timestamp,
            tec.satellite,
            tec.phase_tec,
            tec.p_range_tec) for tec in elem]
        
        publishing_string = '|'.join(elem)
        while True:
            if time.time() % 30 < 0.1:
                client.publish(station, publishing_string)
                print(f"\nSystemTime:{datetime.now()} \nTime: {time.time() % 30}\n")
                print('Published:', publishing_string)
                time.sleep(1)
                break
            else:
                time.sleep(0.1)

        schedule.run_pending()
        elem = next(arr)
