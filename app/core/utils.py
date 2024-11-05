import pandas as pd
import json
import yfinance as yf
from fastapi import Request


class DateTimeDecoder(json.JSONDecoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()  # Converts to 'YYYY-MM-DDTHH:MM:SS'
        return super().default(obj)
    


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)
    


def conver_date_to_datetime(records_retrieved: list[dict]) -> list[dict]:
    for record in records_retrieved:
        if 'Date' in record:
            record['Date'] = pd.to_datetime(record['Date'])
    return records_retrieved


async def get_cache_data(redis_client: Request, key: str, symbol : str, interval: int, span_time: str) -> tuple:
    """
    get data from databes.

    return tuple datafram and a boolean to decide if the method should process data or not
    if is true data should be processed if false data shouldn´t be process
    """
    result = await redis_client.get(key)
    if result is not None:
        # TODO: transform string into list of dict
        return conver_date_to_datetime( json.loads(result)), False
    key = key = f"{span_time}:{interval}:{symbol}"
    result = await redis_client.get(key)
    if result is None:
        stock = yf.Ticker(symbol)
        data = stock.history(period=span_time, interval=interval)
        await redis_client.set(key,json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    else:
        data = pd.DataFrame(conver_date_to_datetime( json.loads(result)))
    return data, True