# Crypto Pipeline

A small Python pipeline that fetches cryptocurrency market data from the
[CoinGecko API](https://www.coingecko.com/en/api) and inserts it into
PostgreSQL. Each run requests the 50 highest-market-cap coins in USD, including
market data and 1-hour, 24-hour, and 7-day price changes.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL
- Network access to the CoinGecko API

## Setup

Clone the repository, then install the project dependencies:

```shell
uv sync
```

Create a PostgreSQL database (the default name is `crypto`), then create a
`.env` file in the project root:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

The database connection settings default to `localhost:5432`, database
`crypto`, and user `postgres`. Set `DB_PASSWORD` to the password for that
PostgreSQL user. Keep `.env` private; it is excluded from Git.

## Run

From the project root, run the ingestion pipeline with:

```shell
uv run python src/ingestion/pipeline.py
```

On Windows PowerShell, the equivalent path is:

```powershell
uv run python src\ingestion\pipeline.py
```

The pipeline fetches the data with retries, creates the `markets` table if it
does not exist, and upserts records by CoinGecko coin ID. Existing records have
their market values and `updated_at` refreshed. Progress and failures are
written to the console log.

## Database table

The pipeline creates a `markets` table with a unique CoinGecko coin ID,
symbol, name, current price, market capitalization and rank, volume, price
changes, and ingestion/update timestamps.

## Project layout

```text
src/
  crypto_pipeline/       Package entry point
  ingestion/             API client, database setup, and ingestion pipeline
data/                    Local data; excluded from Git
pyproject.toml            Project metadata and dependencies
uv.lock                   Locked dependency versions
```