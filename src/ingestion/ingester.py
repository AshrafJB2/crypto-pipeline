import logging
from psycopg2.extras import execute_batch

log = logging.getLogger(__name__)


class DataIngester:
    def __init__(self, conn):
        self.conn = conn

    def ingest_markets(self, data: list[dict]):
        """Ingest cryptocurrency market data into PostgreSQL."""
        records = []
        for coin in data:
            records.append((
                coin.get("id"),
                coin.get("symbol", "").upper(),
                coin.get("name"),
                coin.get("current_price"),
                coin.get("market_cap"),
                coin.get("market_cap_rank"),
                coin.get("total_volume"),
                coin.get("price_change_percentage_1h_in_currency"),
                coin.get("price_change_percentage_24h_in_currency"),
                coin.get("price_change_percentage_7d_in_currency"),
            ))

        with self.conn.cursor() as cur:
            execute_batch(
                cur,
                """
                INSERT INTO markets 
                (coin_id, symbol, name, current_price, market_cap, market_cap_rank,
                 total_volume, price_change_percentage_1h, price_change_percentage_24h,
                 price_change_percentage_7d)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (coin_id) DO UPDATE SET
                    current_price = EXCLUDED.current_price,
                    market_cap = EXCLUDED.market_cap,
                    market_cap_rank = EXCLUDED.market_cap_rank,
                    total_volume = EXCLUDED.total_volume,
                    price_change_percentage_1h = EXCLUDED.price_change_percentage_1h,
                    price_change_percentage_24h = EXCLUDED.price_change_percentage_24h,
                    price_change_percentage_7d = EXCLUDED.price_change_percentage_7d,
                    updated_at = CURRENT_TIMESTAMP
                """,
                records,
                page_size=50,
            )
        self.conn.commit()
        log.info("Ingested %d records into markets table", len(records))
