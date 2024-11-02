import json
from fastapi import APIRouter, Request
from app.core.utils import DateTimeEncoder, conver_date_to_datetime
from trading.indicators.mean_reversion import MeanReversion
from trading.strategies.bolling_strategy import BollingStrategy
from trading.strategies.crossover_strategy import CrossoverStrategy
from trading.indicators.moving_averages import MOVING_AVERAGES, MovingAverages
from trading.performance.calculate_performance import Performance
import yfinance as yf

router = APIRouter()

@router.get("/strategy/crossover/{indicator}/{symbol}")
async def get_crossover_strategy_performance(symbol: str, request: Request, indicator:str='sma', short_period: int = 20, long_period: int = 50,span_time:str='1y', interval:str='1d') -> list[dict]:
    redis_client = request.app.state.redis
    key = f"performance:{indicator}:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    result = await redis_client.get(key)
    if result is not None:
        return conver_date_to_datetime( json.loads(result))
    key = key = f"{span_time}:{interval}:{symbol}"
    result = await redis_client.get(key)
    if result is None:
        stock = yf.Ticker(symbol)
        data = stock.history(period=span_time, interval=interval)
        await redis_client.set(key,json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    strategy = CrossoverStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(MovingAverages, indicator)
    performance = Performance(strategy_data)
    data =  performance.calculate_performance()
    key = f"performance:{indicator}:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    await redis_client.set(key,json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    return data.reset_index().to_dict(orient='records')

@router.get("/strategy/crossover/risk/{symbol}")
async def get_crossover_strategy_risk(symbol: str, request: Request, short_period: int = 20, long_period: int = 50,span_time:str='1y', interval:str='1d') -> dict:
    redis_client = request.app.state.redis
    key = f"strategy:risk:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    result = await redis_client.get(key)
    if result is not None:
        return conver_date_to_datetime( json.loads(result))
    key = key = f"{span_time}:{interval}:{symbol}"
    result = await redis_client.get(key)
    if result is None:
        stock = yf.Ticker(symbol)
        data = stock.history(period=span_time, interval=interval)
        await redis_client.set(key, json.dumps(data.to_dict()))
    strategy = CrossoverStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(MovingAverages, MOVING_AVERAGES.SMA)
    performance = Performance(strategy_data)
    performance.calculate_performance()
    data = performance.calculate_risk()
    key = f"strategy:risk:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    await redis_client.set(key,json.dumps(data.to_dict()))
    return data.to_dict()

@router.get("/strategy/bolling/mre/{symbol}")
async def get_crossover_strategy_performance(symbol: str, request: Request, short_period: int = 20, long_period: int = 50,span_time:str='1y', interval:str='1d') -> list[dict]:
 
    redis_client = request.app.state.redis
    key = f"strategy:risk:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    result = await redis_client.get(key)
    if result is not None:
        return conver_date_to_datetime( json.loads(result))
    key = key = f"{span_time}:{interval}:{symbol}"
    result = await redis_client.get(key)
    if result is None:
        stock = yf.Ticker(symbol)
        data = stock.history(period=span_time, interval=interval)
        await redis_client.set(key, json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    strategy = BollingStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(MeanReversion)
    performance = Performance(strategy_data)
    data =  performance.calculate_performance()
    await redis_client.set(key, json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    return data.reset_index().to_dict(orient='records')
