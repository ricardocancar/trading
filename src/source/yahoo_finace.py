import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import date
from loguru import logger

_DB_DIR = Path(__file__).parent.parent / 'db'

def _cache_path(start: str, end: str) -> Path:
    today = date.today().isoformat()
    return _DB_DIR / f'{today}_{start}_{end}.parquet'

def get_current_gold_price() -> float:
    """Return the latest gold (GC=F) price from Yahoo Finance."""
    ticker = yf.Ticker('GC=F')
    return float(ticker.fast_info['last_price'])


def download_gold_data(start: str | None = None, end: str | None = None) -> pd.DataFrame:
    """Download historical gold (GC=F) data from Yahoo Finance."""
    if not start:
        start = f'{date.today().year}-01-01'
    if not end:
        end = date.today().isoformat()
    cache = _cache_path(start, end)
    if cache.exists():
        logger.info('Loading gold data from cache: {}', cache.name)
        return pd.read_parquet(cache)

    logger.info('Downloading gold data from Yahoo Finance ({} to {})...', start, end)
    data = yf.download('GC=F', start=start, end=end, progress=False)

    _DB_DIR.mkdir(parents=True, exist_ok=True)
    data.to_parquet(cache)
    return data

