import logging
import os

import psycopg2
from psycopg2.extras import execute_batch

log = logging.getLogger(__name__)


class DatabaseConnection:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Establish PostgreSQL connection using environment variables."""
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "crypto"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
        )
        log.info("Connected to PostgreSQL database")
        return self.conn

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            log.info("Closed database connection")

    def get_connection(self):
        """Get the current connection."""
        return self.conn
