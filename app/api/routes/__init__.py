from fastapi import APIRouter
from app.api.routes import stock_data

router = APIRouter()
router.include_router(stock_data.router, prefix="/stocks", tags=["stocks"])