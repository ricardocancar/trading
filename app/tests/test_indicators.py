import pandas as pd
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.api.routes.indicators import router

# Create a FastAPI app and include the router
app = FastAPI()
app.include_router(router)

# Use TestClient to test the FastAPI app
client = TestClient(app)

@pytest.fixture
def mock_redis_client():
    # Create a mock Redis client
    return AsyncMock()

@pytest.fixture
def mock_get_cache_data():
    # Create a mock for the get_cache_data function
    return AsyncMock(return_value=(pd.DataFrame({'Close': [100, 102, 101, 105, 107]}), True ))

@pytest.mark.asyncio
async def test_get_sma(mock_redis_client, mock_get_cache_data):
    # Patch the get_cache_data function
    with patch('app.api.routes.indicators.get_cache_data', mock_get_cache_data):
        # Set the mock Redis client in the app state
        app.state.redis = mock_redis_client

        # Simulate a GET request to the /sma/{symbol} endpoint
        response = client.get("/sma/AAPL?short_period=20&long_period=50&span_time=1y&interval=1d")

        # Assert that the response status code is 200
        assert response.status_code == 200

        # Assert that the response data is in the expected format
        response_data = response.json()
        assert isinstance(response_data, list)
        assert 'sma_short' in response_data[0]
        assert 'sma_long' in response_data[0]

        # Verify that the Redis client set method was called
        mock_redis_client.set.assert_called_once()