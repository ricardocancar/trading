from fastapi import APIRouter
import yfinance as yf

router = APIRouter()

@router.get("/{simbol}")
async def get_stock_data(simbol:str, period:str='1y', interval:str='1d')->list[dict]:
    """
    Get stock data using Yahoo Finance API.

    :param simbol: Stock symbol (e.g., 'AAPL' for Apple)
    :param period: Time period for the data (default '1y' for one year)
    :param interval: Time interval between data points (default '1d' for daily)
    :return: DataFrame of Pandas with historical stock data
    """
    stock = yf.Ticker(simbol)
    data = stock.history(period=period, interval=interval)
    data_with_index = data.reset_index()
    return data_with_index.to_dict(orient='records')