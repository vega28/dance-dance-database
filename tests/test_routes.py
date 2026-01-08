"""Tests for API routes."""
import pytest


class TestHelloRoute:
    def test_hello_returns_message(self, client):
        """Test that /api/hello returns a message."""
        response = client.get('/api/hello')
        assert response.status_code == 200
        assert response.json == {'message': 'hello from flask!'}


class TestSongsRoute:
    def test_songs_returns_list(self, client):
        """Test that /api/songs returns a list of songs."""
        response = client.get('/api/songs')
        assert response.status_code == 200
        songs = response.json
        assert isinstance(songs, list)
        assert len(songs) == 4

    def test_songs_have_required_fields(self, client):
        """Test that each song has required fields."""
        response = client.get('/api/songs')
        songs = response.json
        for song in songs:
            assert 'id' in song
            assert 'title' in song
            assert 'artist' in song
            assert 'status' in song
