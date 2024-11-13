import pandas as pd
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.api.routes.performance import router

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
async def test_get_bolling_strategy_performance(mock_redis_client, mock_get_cache_data):
    with patch('app.api.routes.performance.get_cache_data', mock_get_cache_data):
        app.state.redis = mock_redis_client

        response = client.get("/strategy/bolling/mre/AAPL?short_period=20&long_period=50&span_time=1y&interval=1d")

        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)

        mock_redis_client.set.assert_called_once()
    