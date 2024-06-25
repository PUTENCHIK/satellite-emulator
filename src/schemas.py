from pydantic import BaseModel
from datetime import date


class StartEmulation(BaseModel):
    start_date: date
    stations: list
