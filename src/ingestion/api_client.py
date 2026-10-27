import logging
import time

import requests

log = logging.getLogger(__name__)


class APIClient:
    def __init__(self, url: str, params: dict):
        self.url = url
        self.params = params

    def fetch_with_retry(self, max_retries: int = 3) -> list[dict]:
        """Call the API with exponential backoff."""
        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.get(self.url, params=self.params, timeout=10)
                resp.raise_for_status()
                log.info("Successfully fetched data from API")
                return resp.json()
            except requests.RequestException as e:
                log.warning("Attempt %d/%d failed: %s", attempt, max_retries, e)
                if attempt == max_retries:
                    raise
                sleep_for = 2 ** attempt
                log.info("Retrying in %ds...", sleep_for)
                time.sleep(sleep_for)
