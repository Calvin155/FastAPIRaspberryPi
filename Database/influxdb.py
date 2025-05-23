from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta
import logging


# Docker container address - Internal
INFLUXDB_URL = "http://52.212.232.158:8086"
# Read Only Token
INFLUXDB_TOKEN="RgX7vKr0GqPxbk5vih8nVG7RUylhYzeh5NlO2B6TVH6wEZWyCe7d8_Lpol3fnwdij-KvBdl4g8YIG-VbLa8-Ng=="
INFLUXDB_ORG = "AQI"
INFLUXDB_BUCKET = "AQIMetrics"

class InfluxDB:
    def __init__(self):
        self.url = INFLUXDB_URL
        self.token = INFLUXDB_TOKEN
        self.org = INFLUXDB_ORG
        self.bucket = INFLUXDB_BUCKET
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org, timeout=30_000)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def connect(self):
        try:
            if self.client:
                self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
                logging.info("Successfully Connected to Influx Database")
            else:
                logging.info("Already connected to Influx Database")
        except Exception as e:
            logging.exception("Error Connecting to Database: " + str(e))

    #-----------------------------------------Particulate Matter data ----------------------------------
    def get_pm_data(self):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -15s, stop: now())
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "PM1" or r["_field"] == "PM2.5" or r["_field"] == "PM10")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''

        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            logging.info(result)
            return result
        except Exception as e:
            logging.exception(f"Error while fetching data: {e}")
            return []

    #Will return all 3 Particulate Matter features
    def get_historical_pm_data_by_data(self, start_date, stop_date):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: {start_date}, stop: {stop_date})
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "PM1" or r["_field"] == "PM2.5" or r["_field"] == "PM10")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''

        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            logging.info(result)
            return result
        except Exception as e:
            logging.exception(f"Error while fetching data: {e}")
            return []


    def get_historical_pm1_data_by_data(self, start_date, stop_date):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: {start_date}, stop: {stop_date})
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "PM1")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''

        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            logging.info(result)
            return result
        except Exception as e:
            logging.exception(f"Error while fetching data: {e}")
            return []
        
    def get_historical_pm2_5_data_by_data(self, start_date, stop_date):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: {start_date}, stop: {stop_date})
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "PM2.5")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''

        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            logging.info(result)
            return result
        except Exception as e:
            logging.exception(f"Error while fetching data: {e}")
            return []
        
        
    def get_historical_pm10_data_by_data(self, start_date, stop_date):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: {start_date}, stop: {stop_date})
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "PM10")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''

        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            logging.info(result)
            return result
        except Exception as e:
            logging.exception(f"Error while fetching data: {e}")
            return []
    #-----------------------------------------CO2 data ----------------------------------
    def get_co2_data(self):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -15s, stop: now())
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "Co2 - Parts Per-Million" or r["_field"] == "Co2 Percentage")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 15s, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''
        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            logging.info(result)
            return result
        except Exception as e:
            logging.exception(f"Error while fetching data: {e}")
            return []
        
    def get_historical_co2_ppm_data(self,start_date, stop_date):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: {start_date}, stop: {stop_date})
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "Co2 - Parts Per-Million")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 15s, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''
        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            logging.info(result)
            return result
        except Exception as e:
            logging.exception(f"Error while fetching data: {e}")
            return []
        
    def get_co2_percentage_data(self,start_date, stop_date):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: {start_date}, stop: {stop_date})
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "Co2 Percentage")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 15s, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''
        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            logging.info(result)
            return result
        except Exception as e:
            logging.exception(f"Error while fetching data: {e}")
            return []

    def close(self):
        if self.client:
            self.client.close()
            logging.info("Connection to Database Closed")