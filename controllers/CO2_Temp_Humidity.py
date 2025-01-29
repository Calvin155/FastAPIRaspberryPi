from fastapi import APIRouter, HTTPException
from typing import List
from Database.influxdb import InfluxDB
from models.AQIData import AQIData

class CO2TempHumidityController:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/aqi_co2_temp_humidity_data", self.read_co2_temp_humidity_data, methods=["GET"])

    async def read_co2_temp_humidity_data(self) -> List[AQIData]:
        influx_db = InfluxDB()
        try:
            data = influx_db.get_co2_temp_humidity_data()
            aqi_list = []
            
            for table in data:
                for record in table.records:
                    aqi_list.append(AQIData(time=record.get_time().isoformat(), value=record.get_value()))
            
            return aqi_list
        
        except Exception as e:
            print(f"Error fetching AQI data: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

