import pytest
import pandas as pd
import numpy as np
from trading.performance.calculate_performance import Performance
from trading.performance.base_performance import BasePerformance

@pytest.fixture
def sample_data():
    # Create a sample DataFrame with 'Close' and 'signal' columns
    data = pd.DataFrame({
        'Close': [100, 102, 101, 105, 107],
        'signal': [1, 0, 1, 1, 0]
    })
    return data

def test_base_performance_initialization(sample_data):
    base_perf = BasePerformance(sample_data)
    pd.testing.assert_frame_equal(base_perf.data, sample_data)

def test_calculate_returns(sample_data):
    perf = Performance(sample_data)
    result = perf.calculate_returns()
    expected_returns = sample_data['Close'].pct_change()
    expected_strategy_returns = expected_returns * sample_data['signal'].shift(1)
    pd.testing.assert_series_equal(result['returns'], expected_returns, check_names=False)
    pd.testing.assert_series_equal(result['strategy_returns'], expected_strategy_returns, check_names=False)

def test_calculate_risk(sample_data):
    perf = Performance(sample_data)
    perf.calculate_returns()  # Ensure returns are calculated first
    result = perf.calculate_risk()
    expected_risk = (perf.data[['returns', 'strategy_returns']].apply(np.exp) - 1).std() * 252 ** 0.5
    pd.testing.assert_series_equal(result, expected_risk)

def test_calculate_drawdown(sample_data):
    perf = Performance(sample_data)
    perf.calculate_returns()  # Ensure returns are calculated first
    result = perf.calculate_drawdown()
    expected_cumret = result['strategy_returns'].cumsum().apply(np.exp)
    expected_cummax = expected_cumret.cummax()
    expected_drawdown = expected_cummax - expected_cumret
    pd.testing.assert_series_equal(result['cumret'], expected_cumret, check_names=False)
    pd.testing.assert_series_equal(result['cummax'], expected_cummax, check_names=False)
    pd.testing.assert_series_equal(result['drawdown'], expected_drawdown, check_names=False)

def test_calculate_performance(sample_data):
    perf = Performance(sample_data)
    result = perf.calculate_performance()
    assert 'returns' in result.columns
    assert 'strategy_returns' in result.columns
    assert 'cumret' in result.columns
    assert 'cummax' in result.columns
    assert 'drawdown' in result.columns