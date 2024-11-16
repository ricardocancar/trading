import json
from fastapi import APIRouter, Request
import yfinance as yf

from app.core.utils import DateTimeEncoder, conver_date_to_datetime

router = APIRouter()

@router.get("/{simbol}")
async def get_stock_data(simbol:str,request: Request, period:str='1y', interval:str='1d')->list[dict]:
    """
    Get stock data using Yahoo Finance API.

    :param simbol: Stock symbol (e.g., 'AAPL' for Apple)
    :param period: Time period for the data (default '1y' for one year)
    :param interval: Time interval between data points (default '1d' for daily)
    :return: DataFrame of Pandas with historical stock data
    """
    redis_client = request.app.state.redis
    key = f"{period}:{interval}:{simbol}"
    result = await redis_client.get(key)
    if result is None:
        stock = yf.Ticker(simbol)
        data = stock.history(period=period, interval=interval)
        await redis_client.set(key,json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
        return data.reset_index().to_dict(orient='records')
    return conver_date_to_datetime( json.loads(result))