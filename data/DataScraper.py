import json
import requests
import os
import csv

from dotenv import load_dotenv

class ApiHandler():
    def __init__(self, api_endpoint) -> None:
        load_dotenv()
        self.api_endpoint = api_endpoint
        self.db_path = os.getenv("DB_URI")

    def call_api(self):
        headers = {
            'User-Agent': 'Osrs AlgoTrading',
            'From': 'dcadams@memphis.edu'
        }
        print("Starting api call...")
        response = requests.get(self.api_endpoint, headers=headers)
        if response.status_code == 200:
            print("Data pulled successfully")
            return json.loads(response.content)
        else:
            response.raise_for_status()

    def write_to_csv(self, first_row=None):
        json_data = self.call_api()
        print("Writing data to csv...")
        with open("market_data.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["item_id", "avg_high_price", "high_price_volume", "avg_low_price", "low_price_volume",
                 "timestamp"])

            for symbol, data in json_data["data"].items():
                avg_high_price = data["avgHighPrice"]
                high_price_volume = data["highPriceVolume"]
                avg_low_price = data["avgLowPrice"]
                low_price_volume = data["lowPriceVolume"]
                timestamp = json_data["timestamp"]

                writer.writerow(
                    [symbol, avg_high_price, high_price_volume, avg_low_price, low_price_volume, timestamp])
            print("Writing csv data complete")
            csvfile.close()