from fastapi import APIRouter, HTTPException
from typing import List
from Database.influxdb import InfluxDB
from models.AQIData import AQIData
import logging

class ParticulateMatterRestController:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/aqi_pm_data", self.get_pm_data, methods=["GET"])
        self.router.add_api_route("/aqi_historical_pm_data", self.get_historical_pm_data, methods=["GET"])

    async def get_pm_data(self) -> List[AQIData]:
        influx_db = InfluxDB()
        try:
            data = influx_db.get_pm_data()
            aqi_list = []
            
            for table in data:
                for record in table.records:
                    aqi_list.append(AQIData(time=record.get_time().isoformat(), value=record.get_value()))
            
            return aqi_list
        
        except Exception as e:
            logging.exception(f"Error fetching AQI data: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_historical_pm_data(self) -> List[AQIData]:
        influx_db = InfluxDB()
        try:
            data = influx_db.get_historical_2w_pm_data()
            aqi_list = []
            
            for table in data:
                for record in table.records:
                    aqi_list.append(AQIData(time=record.get_time().isoformat(), value=record.get_value()))
            
            return aqi_list
        
        except Exception as e:
            logging.exception(f"Error fetching AQI data: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

