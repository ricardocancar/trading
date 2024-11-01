from fastapi import APIRouter
from app.api.routes import indicators, stock_data, performance, redis_cache

router = APIRouter()
router.include_router(stock_data.router, prefix="/stocks", tags=["stocks"])
router.include_router(indicators.router, prefix="/indicators", tags=["indicators"])
router.include_router(performance.router, prefix="/performance", tags=["performance"])
router.include_router(redis_cache.router, prefix="/cache", tags=["cache"])
