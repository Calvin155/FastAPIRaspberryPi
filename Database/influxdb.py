from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta
import logging

# Database connection
# INFLUXDB_TOKEN = "BocuA2JSjjFDITXknBnL9E1X4ADJoNEkJe5IrvNisBSfutGqSOvDZ8EZUccUo76Oc-WBsw-HM2PF9BWGH8VdhQ=="
INFLUXDB_TOKEN="7KoJpNuWfJmldZL5-VhLyHQYk-i97ttvJ29Dep0fJ85yJv89_uB0FabyBXMN7x_-hRV7vvDZHSsRw2PTHW14cg=="
INFLUXDB_URL = "http://127.0.0.1:8086"
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
                print("Successfully connected to Influx")
            else:
                logging.info("Already connected to Influx Database")
                print("Already connected to Influx")
        except Exception as e:
            logging.error("Error Connecting to Database: " + str(e))

    def get_pm_data(self):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -1h, stop: now())
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "PM1" or r["_field"] == "PM2.5" or r["_field"] == "PM10")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''

        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            return result
        except Exception as e:
            print(f"Error while fetching data: {e}")
            return []


    def get_co2_temp_humidity_data(self):
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -15s, stop: now())
        |> filter(fn: (r) => r["_measurement"] == "air_quality")
        |> filter(fn: (r) => r["_field"] == "CO2" or r["_field"] == "Temperature" or r["_field"] == "Humidity")
        |> filter(fn: (r) => r["location"] == "local")
        |> aggregateWindow(every: 15s, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''

        try:
            result = self.query_api.query(query, org=INFLUXDB_ORG)
            return result
        except Exception as e:
            print(f"Error while fetching data: {e}")
            return []

    def close(self):
        if self.client:
            self.client.close()
            logging.info("Connection to Database Closed")