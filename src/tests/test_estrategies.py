import pytest
import pandas as pd
import numpy as np
from trading.strategies.bolling_strategy import BollingStrategy
from trading.strategies.crossover_strategy import CrossoverStrategy
from trading.indicators.base_indicator import BaseIndicator
from trading.strategies.base_strategy import BaseStrategy


class MockIndicator(BaseIndicator):
    def calculate(self, *args, **kwargs):
        # Mock calculation for testing purposes
        return pd.DataFrame({"Lower Band": self.data - 1, "Upper Band": self.data + 1})


@pytest.fixture
def sample_data():
    # Create a sample DataFrame with 'Close' column
    data = pd.DataFrame({"Close": [100, 102, 101, 105, 107]})
    return data


def test_bolling_strategy_generate_signals(sample_data):
    strategy = BollingStrategy(sample_data, short_period=5, long_period=20)
    result = strategy.generate_signals(MockIndicator, column_indicator="Close")

    expected_signals = np.array([0, 0, 0, 0, 0])
    expected_positions = np.array([np.nan, 0, 0, 0, 0])

    np.testing.assert_array_equal(result["signal"].values, expected_signals)
    np.testing.assert_array_equal(result["positions"].values, expected_positions)


def test_crossover_strategy_generate_signals(sample_data):
    class MockCrossoverIndicator(BaseIndicator):
        def calculate(self, period, mode):
            return self.data.rolling(window=period).mean()

    strategy = CrossoverStrategy(sample_data, short_period=2, long_period=3)
    result = strategy.generate_signals(
        MockCrossoverIndicator, mode=None, column_indicator="Close"
    )

    expected_signals = np.array([0, 0, 1, 1, 1])
    expected_positions = np.array([np.nan, 0, 1, 0, 0])

    np.testing.assert_array_equal(result["signal"].values, expected_signals)
    np.testing.assert_array_equal(result["positions"].values, expected_positions)


def test_base_strategy_abstract_method():
    with pytest.raises(TypeError):
        BaseStrategy(pd.DataFrame())
