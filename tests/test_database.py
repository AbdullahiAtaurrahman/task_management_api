import pytest
from sqlalchemy import text

from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_test_database_connection():
    async with TestingSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))

        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_database_transaction_rollback(db_session):
    from sqlalchemy import text

    connection = await db_session.connection()

    await db_session.execute(text("SELECT 1"))

    await db_session.commit()

    assert connection.in_transaction()
