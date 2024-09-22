import pandas as pd
from indicators.moving_averages import MovingAverages


def test_moving_average_sma():
    # Sample data for testing
    data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    moving_averages = MovingAverages(data)

    # Calculate the Simple Moving Average (SMA) for a period of 3
    sma_result = moving_averages.sma(period=3)

    # Expected result
    expected_result = pd.Series([None, None, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
    
    # Assert that the calculated SMA matches the expected result
    pd.testing.assert_series_equal(sma_result, expected_result)

def test_moving_average_ema():
    # Sample data for testing
    data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    moving_averages = MovingAverages(data)

    # Calculate the Exponential Moving Average (EMA) for a period of 3
    ema_result = moving_averages.ema(period=3)

    # Expected result (calculated manually or using a reliable source)
    expected_result = pd.Series([1.0, 1.5, 2.25, 3.125, 4.0625, 5.03125, 6.015625, 7.0078125, 8.00390625, 9.001953125])

    # Assert that the calculated EMA matches the expected result
    pd.testing.assert_series_equal(ema_result, expected_result)
