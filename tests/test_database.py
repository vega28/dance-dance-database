"""Tests for database connection."""
import pytest
from sqlalchemy import text


class TestDatabaseConnection:
    def test_database_connection(self, app_context):
        """Test that the database connection is working."""
        from api.api import db
        try:
            result = db.session.execute(text('SELECT 1'))
            assert result.scalar() == 1
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")

    def test_database_session_is_active(self, app_context):
        """Test that a database session can be created."""
        from api.api import db
        assert db.session.is_active
