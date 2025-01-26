from fastapi import FastAPI
from influxdb_client import InfluxDBClient
from pydantic import BaseModel
from typing import List
from datetime import datetime

INFLUXDB_URL = "http://192.168.1.35:8086"
INFLUXDB_TOKEN = "7KoJpNuWfJmldZL5-VhLyHQYk-i97ttvJ29Dep0fJ85yJv89_uB0FabyBXMN7x_-hRV7vvDZHSsRw2PTHW14cg=="
INFLUXDB_ORG = "AQI"
INFLUXDB_BUCKET = "AQIMetrics"

app = FastAPI()

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

def get_aqi_data():
    query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: -15s)'
    result = client.query_api().query(query, org=INFLUXDB_ORG)
    return result

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
    data = get_aqi_data()
    aqi_list = []
    for table in data:
        for record in table.records:
            aqi_list.append(AQIData(time=record.get_time().isoformat(), value=record.get_value()))
    return aqi_list
