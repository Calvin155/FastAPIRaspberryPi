from fastapi import FastAPI
from influxdb_client import InfluxDBClient
from pydantic import BaseModel
from typing import List
from datetime import datetime
from Database.influxdb import InfluxDB

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


class AQIData(BaseModel):
    time: str
    value: float
    @classmethod
    def parse_obj(cls, obj):
        if isinstance(obj['time'], datetime):
            obj['time'] = obj['time'].isoformat()
        return super().parse_obj(obj)


@app.get("/aqi", response_model=List[AQIData])
async def read_aqi():
    try:
        influx = InfluxDB()
        data = influx.get_aqi_data()
        aqi_list = []
        for table in data:
            for record in table.records:
                aqi_list.append(AQIData(time=record.get_time().isoformat(), value=record.get_value()))
        return aqi_list
    except Exception as e:
        print(e)
