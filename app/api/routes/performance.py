from fastapi import APIRouter
from trading.indicators.mean_reversion import MeanReversion
from trading.strategies.bolling_strategy import BollingStrategy
from trading.strategies.crossover_strategy import CrossoverStrategy
from trading.indicators.moving_averages import MOVING_AVERAGES, MovingAverages
from trading.performance.calculate_performance import Performance
import yfinance as yf

router = APIRouter()

@router.get("/strategy/crossover/{indicator}/{symbol}")
async def get_crossover_strategy_performance(symbol: str, indicator:str='sma', short_period: int = 20, long_period: int = 50,span_time:str='1y', interval:str='1d') -> list[dict]:
 
    stock = yf.Ticker(symbol)
    data = stock.history(period=span_time, interval=interval)
    strategy = CrossoverStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(MovingAverages, indicator)
    performance = Performance(strategy_data)
    data =  performance.calculate_performance()
    return data.reset_index().to_dict(orient='records')

@router.get("/strategy/crossover/risk/{symbol}")
async def get_crossover_strategy_risk(symbol: str, short_period: int = 20, long_period: int = 50,span_time:str='1y', interval:str='1d') -> dict:
    stock = yf.Ticker(symbol)
    data = stock.history(period=span_time, interval=interval)
    strategy = CrossoverStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(MovingAverages, MOVING_AVERAGES.SMA)
    performance = Performance(strategy_data)
    performance.calculate_performance()
    data = performance.calculate_risk()
    return data.to_dict()

@router.get("/strategy/bolling/mre/{symbol}")
async def get_crossover_strategy_performance(symbol: str, short_period: int = 20, long_period: int = 50,span_time:str='1y', interval:str='1d') -> list[dict]:
 
    stock = yf.Ticker(symbol)
    data = stock.history(period=span_time, interval=interval)
    strategy = BollingStrategy(data, short_period, long_period)
    strategy_data = strategy.generate_signals(MeanReversion)
    performance = Performance(strategy_data)
    data =  performance.calculate_performance()
    return data.reset_index().to_dict(orient='records')
