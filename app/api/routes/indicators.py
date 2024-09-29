from fastapi import APIRouter
from trading.indicators.moving_averages import MovingAverages
import yfinance as yf

router = APIRouter()

@router.get("/sma/{symbol}")
async def get_sma(symbol: str, short_period: int = 20, long_period: int = 50, span_time:str='1y', interval:str='1d') -> list[dict]:
    """
    Get Simple Moving Average (SMA) for a given stock symbol.

    :param symbol: Stock symbol (e.g., 'AAPL' for Apple)
    :param short_period: Time period for the short SMA (default is 20 days)
    :param long_period: Time period for the long SMA (default is 50 days)
    :param span_time: Time span for the data (default is '1y' for one year)
    :param interval: Time interval between data points (default is '1d' for daily)
    """
    stock = yf.Ticker(symbol)
    data = stock.history(period=span_time, interval=interval)
    long_sma = MovingAverages(data=data['Close']).sma(long_period)
    short_sma = MovingAverages(data=data['Close']).sma(short_period)
    data['sma_short'] = short_sma
    data['sma_long'] = long_sma

    return data.reset_index().to_dict(orient="records")