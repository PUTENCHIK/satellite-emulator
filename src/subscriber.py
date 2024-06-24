import requests
import paho.mqtt.client as mqtt_client

from config import settings


def check_client_activity():
    curtime = time.time()
    for client, last_message_time in last_message_times.items():
        if curtime - last_message_time < INACTIVITY_TIMEOUT:
            return True
    return False


def on_message():
    data = str(message.payload.decode("utf-8"))
    print("received message =", data)
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
stations = response.json()['stations']

for station in stations:
    client.subscribe(station)

while True:
    if check_client_activity():
        time.sleep(10)
        continue
    else:
        break

client.disconnect()
client.loop_stop()
