import json
from fastapi import APIRouter, Request
from app.core.utils import DateTimeEncoder, get_cache_data
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
    data, process_data = await get_cache_data(redis_client, key , symbol, interval, span_time)
    if not process_data:
        return data
    strategy = CrossoverStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(MovingAverages, indicator)
    performance = Performance(strategy_data)
    data =  performance.calculate_performance()
    await redis_client.set(key,json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    return data.reset_index().to_dict(orient='records')

@router.get("/strategy/crossover/risk/{indicator}/{symbol}")
async def get_crossover_strategy_risk(symbol: str, request: Request, indicator:str='sma', short_period: int = 20, long_period: int = 50,span_time:str='1y', interval:str='1d') -> dict:
    redis_client = request.app.state.redis
    key = f"strategy:risk:{indicator}:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    data , process_data = await get_cache_data(redis_client, key , symbol, interval, span_time)
    if not process_data:
        return data
    strategy = CrossoverStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(indicator=MovingAverages, mode=MOVING_AVERAGES.SMA.value)
    performance = Performance(strategy_data)
    performance.calculate_performance()
    data = performance.calculate_risk()
    await redis_client.set(key,json.dumps(data.to_dict()))
    return data.to_dict()

@router.get("/strategy/bolling/mre/{symbol}")
async def get_crossover_strategy_performance(symbol: str, request: Request, short_period: int = 20, long_period: int = 50,span_time:str='1y', interval:str='1d') -> list[dict]:
 
    redis_client = request.app.state.redis
    key = f"strategy:risk:{span_time}:{interval}:{symbol}:{short_period}:{long_period}"
    data, process_data = await get_cache_data(redis_client, key , symbol, interval, span_time)
    if not process_data:
        return data
    strategy = BollingStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(MeanReversion)
    performance = Performance(strategy_data)
    data =  performance.calculate_performance()
    await redis_client.set(key, json.dumps(data.reset_index().to_dict(orient="records"), cls=DateTimeEncoder))
    return data.reset_index().to_dict(orient='records')
