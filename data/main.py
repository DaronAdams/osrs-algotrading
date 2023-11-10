from DataScraper import ApiHandler

# Constants ----------------------------------------------------------------
api_endpoint = "https://prices.runescape.wiki/api/v1/osrs/5m"
db_path = "/market_data.db"

handler = ApiHandler(api_endpoint, db_path)
handler.update_database_with_api_data()

