import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from main import app

@pytest.mark.asyncio
async def test_ping():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "test"}
