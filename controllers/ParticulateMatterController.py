from fastapi import APIRouter, HTTPException
from typing import List
from Database.influxdb import InfluxDB
from models.AQIData import AQIData

class ParticulateMatterRestController:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/aqi_pm_data", self.read_pm_data, methods=["GET"])

    async def read_pm_data(self) -> List[AQIData]:
        influx_db = InfluxDB()
        try:
            data = influx_db.get_pm_data()
            aqi_list = []
            
            for table in data:
                for record in table.records:
                    aqi_list.append(AQIData(time=record.get_time().isoformat(), value=record.get_value()))
            
            return aqi_list
        
        except Exception as e:
            print(f"Error fetching AQI data: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

