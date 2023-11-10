import psycopg2
import requests
import os

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
            return response.json()
        else:
            response.raise_for_status()

    def save_to_database(self, data):
        records_to_insert = []

        # Extract the timestamp which is common for all entries
        timestamp = data['timestamp']

        # Iterate over the items excluding the timestamp
        for id, stats in data.items():
            if id != 'timestamp':  # Skip the timestamp entry
                record = (
                    id,
                    stats.get('avgHighPrice'),
                    stats.get('highPriceVolume'),
                    stats.get('avgLowPrice'),
                    stats.get('lowPriceVolume'),
                    timestamp
                )
                records_to_insert.append(record)

        # SQL to insert data
        insert_query = '''
        INSERT INTO market_data (id, avg_high_price, high_price_volume, avg_low_price, low_price_volume, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        '''

        try:
            conn = psycopg2.connect(self.db_path)
            cursor = conn.cursor()
            cursor.executemany(insert_query, records_to_insert)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")

    def update_database_with_api_data(self):
        data = self.call_api()

        # Transform the data as necessary to fit your database schema.
        # This is a placeholder for the data transformation logic.
        # transformed_data = [(item['field1'], item['field2']) for item in data]
        self.save_to_database(data)
