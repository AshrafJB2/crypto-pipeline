import logging
from dotenv import load_dotenv

from api_client import APIClient
from database import DatabaseConnection
from schema import TableManager
from ingester import DataIngester

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "1h,24h,7d",
}


def main():
    """Fetch data from API and ingest directly into PostgreSQL."""
    try:
        log.info("Starting data pipeline...")

        api_client = APIClient(URL, PARAMS)
        data = api_client.fetch_with_retry()

        db_connection = DatabaseConnection()
        conn = db_connection.connect()

        table_manager = TableManager(conn)
        table_manager.create_markets_table()

        ingester = DataIngester(conn)
        ingester.ingest_markets(data)

        db_connection.close()
        log.info("Data pipeline completed successfully")

    except Exception as e:
        log.error("Pipeline failed: %s", e)
        raise


if __name__ == "__main__":
    main()
