from fastapi import APIRouter
from app.api.routes import indicators, stock_data

router = APIRouter()
router.include_router(stock_data.router, prefix="/stocks", tags=["stocks"])
router.include_router(indicators.router, prefix="/indicators", tags=["indicators"])