import pytest
from sqlalchemy import text

from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_test_database_connection():
    async with TestingSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))

        assert result.scalar() == 1
