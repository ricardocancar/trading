from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from loguru import logger

from source.yahoo_finace import download_gold_data, get_current_gold_price
from trading.var.var import (
    calcular_retornos,
    historical_var_percentiles,
    get_operation_num,
    get_averages,
    cent_loss,
)

app = FastAPI(title="Gold Risk Calculator")

STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class RiskRequest(BaseModel):
    capital: float = 80_000
    lotaje: float = 0.02
    min_marging: float = 10_000
    palanca: int = 500
    operation_range: int | None = None  # rango total en pips; si no se provee se calcula desde VaR


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/risk")
def calculate_risk(req: RiskRequest):
    logger.info("Risk calculation request: {}", req)

    gold_price = get_current_gold_price()
    gold = download_gold_data()
    returns = calcular_retornos(gold)
    var = historical_var_percentiles(returns)

    operation_number = get_operation_num(
        capital=req.capital,
        lotaje=req.lotaje,
        min_marging=req.min_marging,
        palanca=req.palanca,
        valor_activo=gold_price,
    )

    std_pips = int(var["std"] * gold_price / 0.10)
    operation_range = req.operation_range if req.operation_range else std_pips * max(operation_number, 1)
    logger.debug(operation_range)
    recommended_averages = max(1, round(operation_range / max(operation_number, 1)))

    loss, operation_range = cent_loss(
        operation_range=operation_range,
        lotaje=req.lotaje,
        operation_number=max(operation_number, 1),
        capital=req.capital
    )

    def pips(pct: float) -> int:
        return int(abs(pct) * gold_price / 0.10)

    def usd(pct: float) -> float:
        return round(abs(pct) * gold_price, 2)

    return {
        "gold_price": round(gold_price, 2),
        "operation_number": operation_number,
        "operation_range": operation_range,
        "recommended_averages": recommended_averages,
        "cent_loss": round(loss, 2),
        "var": {
            "downside_5pct":     round(var["lower_var"] * 100, 3),
            "downside_5pct_usd": usd(var["lower_var"]),
            "downside_5pct_pip": pips(var["lower_var"]),
            "upside_95pct":      round(var["upper_var"] * 100, 3),
            "upside_95pct_usd":  usd(var["upper_var"]),
            "upside_95pct_pip":  pips(var["upper_var"]),
            "extreme_fall":      round(var["worst_day"] * 100, 3),
            "extreme_fall_usd":  usd(var["worst_day"]),
            "extreme_fall_pip":  pips(var["worst_day"]),
            "extreme_rise":      round(var["best_day"] * 100, 3),
            "extreme_rise_usd":  usd(var["best_day"]),
            "extreme_rise_pip":  pips(var["best_day"]),
            "daily_std":         round(var["std"] * 100, 3),
            "daily_std_usd":     usd(var["std"]),
            "daily_std_pip":     pips(var["std"]),
        },
    }
