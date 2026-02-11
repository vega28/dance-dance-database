"""Tests for database connection."""

class TestDatabaseConnection:
    def test_database_connection(self, db_session):
        """Test that the database connection is working."""        
        import pytest
        from sqlalchemy import text
        
        try:
            result = db_session.execute(text('SELECT 1'))
            assert result.scalar() == 1
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")

    def test_database_session_is_active(self, db_session):
        """Test that a database session can be created."""
        assert db_session.is_active
