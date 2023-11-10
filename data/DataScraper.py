import json
import psycopg2
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
        response = requests.get(self.api_endpoint, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            response.raise_for_status()

    def write_to_csv(self, first_row=None):
        json_data = self.call_api()
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

            # Close the CSV file
            csvfile.close()

    # def save_to_database(self, data):
    #     with psycopg2.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #
    #         insert_query = '''
    #             INSERT INTO market_data (item_id, avg_high_price, high_price_volume, avg_low_price, low_price_volume, timestamp)
    #             VALUES (%s, %s, %s, %s, %s, %s)
    #         '''
    #
    #         timestamp = data["timestamp"]
    #
    #         for symbol, data in data["data"].items():
    #             avg_high_price = data["avgHighPrice"]
    #             high_price_volume = data["highPriceVolume"]
    #             avg_low_price = data["avgLowPrice"]
    #             low_price_volume = data["lowPriceVolume"]
    #
    #         cursor.execute(insert_query,
    #                        (symbol, avg_high_price, high_price_volume, avg_low_price, low_price_volume, timestamp))

    # def update_database_with_api_data(self):
    #     data = self.call_api()
    #
    #     self.save_to_database(data)

    # def print_data(self):
    #     with psycopg2.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #
    #         cursor.execute("SELECT * FROM market_data")
    #
    #         records = cursor.fetchall()
    #         for record in records:
    #             print(record)
