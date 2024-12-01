import pytest
import pandas as pd
import numpy as np
from trading.indicators.moving_averages import MovingAverages, MOVING_AVERAGES
from trading.indicators.momentum_indicators import (
    MomentumIndicators,
    MOMENTUM_INDICATORS,
)
from trading.indicators.mean_reversion import MeanReversion
from trading.indicators.base_indicator import BaseIndicator


@pytest.fixture
def sample_data():
    # Create a sample DataFrame with a 'Close' column
    data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return data


def test_sma(sample_data):
    ma = MovingAverages(sample_data)
    result = ma.sma(period=3)
    expected = sample_data.rolling(window=3).mean()
    pd.testing.assert_series_equal(result, expected)


def test_ema(sample_data):
    ma = MovingAverages(sample_data)
    result = ma.ema(period=3)
    expected = sample_data.ewm(span=3, adjust=False).mean()
    pd.testing.assert_series_equal(result, expected)


def test_wma(sample_data):
    ma = MovingAverages(sample_data)
    result = ma.wma(period=3)
    weights = np.arange(1, 4)
    expected = sample_data.rolling(window=3).apply(
        lambda x: np.dot(x, weights) / weights.sum(), raw=True
    )
    pd.testing.assert_series_equal(result, expected)


def test_hma(sample_data):
    ma = MovingAverages(sample_data)
    result = ma.hma(period=3)
    expected = sample_data.rolling(window=3).apply(
        lambda x: np.sqrt(np.dot(x, x) / 3), raw=True
    )
    pd.testing.assert_series_equal(result, expected)


def test_calculate_sma(sample_data):
    ma = MovingAverages(sample_data)
    result = ma.calculate(period=3, mode=MOVING_AVERAGES.SMA.value)
    expected = ma.sma(period=3)
    pd.testing.assert_series_equal(result, expected)


def test_calculate_invalid_mode(sample_data):
    ma = MovingAverages(sample_data)
    with pytest.raises(ValueError, match="Invalid mode: invalid"):
        ma.calculate(period=3, mode="invalid")


def test_base_indicator_initialization(sample_data):
    indicator = BaseIndicator(sample_data)
    pd.testing.assert_series_equal(indicator.data, sample_data)


def test_rsi(sample_data):
    mi = MomentumIndicators(sample_data)
    result = mi.rsi(period=3)
    delta = sample_data.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=3).mean()
    avg_loss = loss.rolling(window=3).mean()
    rs = avg_gain / avg_loss
    expected = 100 - (100 / (1 + rs))
    pd.testing.assert_series_equal(result, expected)


def test_calculate_rsi(sample_data):
    mi = MomentumIndicators(sample_data)
    result = mi.calculate(period=3, mode=MOMENTUM_INDICATORS.RSI)
    expected = mi.rsi(period=3)
    pd.testing.assert_series_equal(result, expected)


def test_calculate_invalid_mode_momentum(sample_data):
    mi = MomentumIndicators(sample_data)
    with pytest.raises(ValueError, match="Invalid mode: invalid"):
        mi.calculate(period=3, mode="invalid")


def test_mean_reversion_calculate(sample_data):
    mr = MeanReversion(sample_data, period=3, num_std_dev=2)
    result = mr.calculate()
    middle_band = sample_data.rolling(window=3).mean()
    rolling_std = sample_data.rolling(window=3).std()
    upper_band = middle_band + (rolling_std * 2)
    lower_band = middle_band - (rolling_std * 2)
    expected = pd.DataFrame(
        {"Middle Band": middle_band, "Upper Band": upper_band, "Lower Band": lower_band}
    )
    pd.testing.assert_frame_equal(result, expected)
