from pydantic import BaseModel
from typing import List

class AQIData(BaseModel):
    time: str
    value: float
