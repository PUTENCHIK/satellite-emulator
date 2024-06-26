import requests
from config import settings


conf = settings()
app_port = conf['app_port']

response = requests.post(f"http://127.0.0.1:{app_port}/update_date")
answer = response.json()
