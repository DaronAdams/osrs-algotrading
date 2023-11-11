from DataScraper import ApiHandler

# Constants ----------------------------------------------------------------
api_endpoint = "https://prices.runescape.wiki/api/v1/osrs/5m"

handler = ApiHandler(api_endpoint)
handler.write_to_csv()