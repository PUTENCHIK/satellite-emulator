import requests
import paho.mqtt.client as mqtt_client
import time
from datetime import datetime

from config import settings


def check_client_activity():
    curtime = time.time()
    for client, last_message_time in last_message_times.items():
        if curtime - last_message_time < INACTIVITY_TIMEOUT:
            return True
    return False


def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print(f"\nReceived data at {datetime.now()}")
    data = data.split("|")
    for i, row in enumerate(data):
        print(f"\t {i+1} row: {row}")
    print("\n")

    last_message_times[message.topic] = time.time()


conf = settings()
last_message_times = {}
INACTIVITY_TIMEOUT = 300


client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1)
client.on_message=on_message
client.connect("localhost", 1883, 60)
client.loop_start()

app_port = conf['app_port']
response = requests.get(f"http://127.0.0.1:{app_port}/get_stations")
try:
    stations = response.json()['stations']
except KeyError:
    print("Can't get stations from app. Most likely it wasn't started")

for station in stations:
    client.subscribe(station)
    last_message_times[station] = time.time()

while True:
    if check_client_activity():
        time.sleep(10)
        continue
    else:
        break

client.disconnect()
client.loop_stop()
exit()
