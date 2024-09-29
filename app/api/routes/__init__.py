from fastapi import APIRouter
from app.api.routes import indicators, stock_data, performance

router = APIRouter()
router.include_router(stock_data.router, prefix="/stocks", tags=["stocks"])
router.include_router(indicators.router, prefix="/indicators", tags=["indicators"])
router.include_router(performance.router, prefix="/performance", tags=["performance"])
