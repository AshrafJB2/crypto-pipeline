import logging

import psycopg2
from psycopg2.extras import execute_batch

log = logging.getLogger(__name__)


class TableManager:
    def __init__(self, conn):
        self.conn = conn

    def create_markets_table(self):
        """Create markets table if it doesn't exist."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS markets (
                    id SERIAL PRIMARY KEY,
                    coin_id VARCHAR(255) UNIQUE,
                    symbol VARCHAR(50),
                    name VARCHAR(255),
                    current_price NUMERIC,
                    market_cap NUMERIC,
                    market_cap_rank INTEGER,
                    total_volume NUMERIC,
                    price_change_percentage_1h NUMERIC,
                    price_change_percentage_24h NUMERIC,
                    price_change_percentage_7d NUMERIC,
                    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        self.conn.commit()
        log.info("Table 'markets' created or verified")
