from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from loguru import logger
from typing import Literal

from source.yahoo_finace import download_gold_data, get_current_gold_price
from trading.var.var import (
    calcular_retornos,
    historical_var_percentiles,
    get_operation_num,
    cent_loss,
    dollar_loss,
    expected_shortfall,
    upper_expected_shortfall,
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
    operation_range: int | None = None
    account_type: Literal["cents", "dollars"] = "cents"


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/chart", response_class=FileResponse)
def chart():
    return FileResponse(STATIC_DIR / "chart.html")


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
    recommended_averages = max(1, round(operation_range / max(operation_number, 1)))

    if req.account_type == "cents":
        loss, operation_range = cent_loss(
            operation_range=operation_range,
            lotaje=req.lotaje,
            operation_number=max(operation_number, 1),
            capital=req.capital,
        )
        loss_display = {"cents": round(loss, 2), "dollars": round(loss / 100, 4)}
    else:
        loss, operation_range = dollar_loss(
            operation_range=operation_range,
            lotaje=req.lotaje,
            operation_number=max(operation_number, 1),
            capital=req.capital,
        )
        loss_display = {"cents": None, "dollars": round(loss, 2)}

    def pips(pct: float) -> int:
        return int(abs(pct) * gold_price / 0.10)

    def usd(pct: float) -> float:
        return round(abs(pct) * gold_price, 2)

    return {
        "gold_price": round(gold_price, 2),
        "account_type": req.account_type,
        "operation_number": operation_number,
        "operation_range": operation_range,
        "recommended_averages": recommended_averages,
        "loss": loss_display,
        "cent_loss": round(loss, 2),  # kept for backwards compat
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


@app.get("/api/levels")
def get_levels():
    """Return current gold price and absolute price levels for VaR/CVaR reference lines."""
    gold_price = get_current_gold_price()
    gold = download_gold_data()
    returns = calcular_retornos(gold)
    var = historical_var_percentiles(returns)
    cvar_lower = expected_shortfall(returns, 5.0)
    cvar_upper = upper_expected_shortfall(returns, 95.0)

    def price_at(pct: float) -> float:
        return round(gold_price * (1 + pct), 2)

    return {
        "gold_price": round(gold_price, 2),
        "levels": {
            "best_day":  price_at(var["best_day"]),
            "cvar_up":   price_at(cvar_upper),
            "var_up":    price_at(var["upper_var"]),
            "var_down":  price_at(var["lower_var"]),
            "cvar_down": price_at(cvar_lower),
            "worst_day": price_at(var["worst_day"]),
        },
        "pct": {
            "best_day":  round(var["best_day"] * 100, 3),
            "cvar_up":   round(cvar_upper * 100, 3),
            "var_up":    round(var["upper_var"] * 100, 3),
            "var_down":  round(var["lower_var"] * 100, 3),
            "cvar_down": round(cvar_lower * 100, 3),
            "worst_day": round(var["worst_day"] * 100, 3),
        },
    }
