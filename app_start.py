import uvicorn
from src.config import settings
from app import app


conf = settings()

try:
    uvicorn.run(app, host="0.0.0.0", port=conf['app_port'])
except:
    print("Unknown error")
    exit()
