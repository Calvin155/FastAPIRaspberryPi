from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import logging
import os

# Database connections
# Local IP address - Database stored on my laptop
# For Local dev/testing
# Change IP address if want raspberry pi to write to local db db on dev machine
# URL = "http://192.168.1.47:8086"
# TOKEN = "BocuA2JSjjFDITXknBnL9E1X4ADJoNEkJe5IrvNisBSfutGqSOvDZ8EZUccUo76Oc-WBsw-HM2PF9BWGH8VdhQ=="

INFLUXDB_URL = "http://192.168.1.35:8086"
INFLUXDB_TOKEN = "7KoJpNuWfJmldZL5-VhLyHQYk-i97ttvJ29Dep0fJ85yJv89_uB0FabyBXMN7x_-hRV7vvDZHSsRw2PTHW14cg=="
INFLUXDB_ORG = "AQI"
INFLUXDB_BUCKET = "AQIMetrics"


class InfluxDB:
    def __init__(self):
        self.url = INFLUXDB_URL
        self.token = INFLUXDB_TOKEN
        self.org = INFLUXDB_ORG
        self.bucket = INFLUXDB_BUCKET
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
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


    def get_aqi_data(self):
        query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: -15s)'
        result = self.query_api().query(query, org=INFLUXDB_ORG)
        return result

    def close(self):
        if self.client:
            self.client.close()
            logging.info("Connection to Database Closed")
