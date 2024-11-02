import json
from fastapi import APIRouter, Request
import pandas as pd
from app.core.utils import DateTimeDecoder, DateTimeEncoder, conver_date_to_datetime
from trading.indicators.moving_averages import MovingAverages
import yfinance as yf

router = APIRouter()




@router.get("/sma/{symbol}")
async def get_sma(symbol: str, request: Request, short_period: int = 20, long_period: int = 50, span_time:str='1y', interval:str='1d') -> list[dict]:
    """
    Get Simple Moving Average (SMA) for a given stock symbol.

    :param symbol: Stock symbol (e.g., 'AAPL' for Apple)
    :param short_period: Time period for the short SMA (default is 20 days)
    :param long_period: Time period for the long SMA (default is 50 days)
    :param span_time: Time span for the data (default is '1y' for one year)
    :param interval: Time interval between data points (default is '1d' for daily)
    """
    redis_client = request.app.state.redis
    key = f"indicator:sma:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    result = await redis_client.get(key)
    if result is not None:
        # TODO: transform string into list of dict
        return conver_date_to_datetime( json.loads(result))
    key = key = f"{span_time}:{interval}:{symbol}"
    result = await redis_client.get(key)
    if result is None:
        stock = yf.Ticker(symbol)
        data = stock.history(period=span_time, interval=interval)
        await redis_client.set(key,json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    else:
        data = pd.Dataframe(conver_date_to_datetime( json.loads(result)))
    long_sma = MovingAverages(data=data['Close']).sma(long_period)
    short_sma = MovingAverages(data=data['Close']).sma(short_period)
    data['sma_short'] = short_sma
    data['sma_long'] = long_sma
    key = f"indicator:sma:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    await redis_client.set(key, json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    return data.reset_index().to_dict(orient="records")