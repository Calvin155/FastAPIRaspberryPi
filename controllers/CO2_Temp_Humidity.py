from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from Database.influxdb import InfluxDB
from models.AQIData import AQIData

class CO2TempHumidityController:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/aqi_co2_data",self.read_co2_data,methods=["GET"])
        self.router.add_api_route("/aqi_co2_temp_humidity_data", self.read_co2_temp_humidity_data, methods=["GET"])
        self.router.add_api_route("/aqi_co2_data",self.read_co2_data,methods=["GET"])
        self.router.add_api_route("/aqi_co2_percentage_data",self.read_co2_percentage_data,methods=["GET"])
        self.router.add_api_route("/aqi_co2_ppm_data",self.read_co2_ppm_data,methods=["GET"])

    async def read_co2_data(self) -> List[AQIData]:
        influx_db = InfluxDB()
        try:
            data = influx_db.get_co2_data()
            return [
                AQIData(time=rec.get_time().isoformat(), value=rec.get_value())
                for table in data
                for rec in table.records
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

    async def read_co2_temp_humidity_data(self) -> List[AQIData]:
        influx_db = InfluxDB()
        try:
            data = influx_db.get_co2_data()
            aqi_list = []
            
            for table in data:
                for record in table.records:
                    aqi_list.append(AQIData(time=record.get_time().isoformat(), value=record.get_value()))
            
            return aqi_list
        
        except Exception as e:
            print(f"Error fetching AQI data: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def read_co2_percentage_data(self,*,start: datetime = Query(...,description="ISO8601",),end: Optional[datetime] = Query(None,description="ISO8601",),) -> List[AQIData]:
        influx_db = InfluxDB()
        try:
            start_s = start.isoformat()
            end_s = end.isoformat() if end else "now()"
            data = influx_db.get_co2_percentage_data(start_s, end_s)
            return [
                AQIData(time=rec.get_time().isoformat(), value=rec.get_value())
                for table in data
                for rec in table.records
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def read_co2_ppm_data(self,*,start: datetime = Query(...,description="ISO8601",),end: Optional[datetime] = Query(None,description="ISO8601",),) -> List[AQIData]:
        influx_db = InfluxDB()
        try:
            start_s = start.isoformat()
            end_s = end.isoformat() if end else "now()"
            data = influx_db.get_historical_co2_ppm_data(start_s, end_s)
            return [
                AQIData(time=rec.get_time().isoformat(), value=rec.get_value())
                for table in data
                for rec in table.records
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
