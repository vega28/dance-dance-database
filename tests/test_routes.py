"""Tests for API routes."""

class TestHelloRoute:
    def test_hello_returns_message(self, client):
        """Test that /api/hello returns a message."""
        response = client.get('/api/hello')
        assert response.status_code == 200
        assert response.json == {'message': 'hello from flask!'}


class TestArtistsRoute:
    def test_artists_returns_list(self, client):
        """Test that /api/artists returns a list of artists."""
        response = client.get('/api/artists')
        assert response.status_code == 200
        artists = response.json
        assert isinstance(artists, list)
        assert len(artists) == 4

    def test_artists_have_required_fields(self, client):
        """Test that each artist has required fields."""
        response = client.get('/api/artists')
        artists = response.json
        for artist in artists:
            assert 'id' in artist
            assert 'name' in artist
            assert 'songs' in artist

    def test_artist_names_match_seed_data(self, client):
        """Test that artist names match seeded data."""
        response = client.get('/api/artists')
        artists = response.json
        artist_names = {a['name'] for a in artists}
        expected_names = {'ATEEZ', 'BTS', 'Chungha', 'Da-Ice'}
        assert artist_names == expected_names


class TestSongsRoute:
    def test_songs_returns_list(self, client):
        """Test that /api/songs returns a list of songs."""
        response = client.get('/api/songs')
        assert response.status_code == 200
        songs = response.json
        assert isinstance(songs, list)
        assert len(songs) == 4
        assert any(s['title'] == 'Wave' for s in response.json)

    def test_songs_have_required_fields(self, client):
        """Test that each song has required fields."""
        response = client.get('/api/songs')
        songs = response.json
        for song in songs:
            assert 'id' in song
            assert 'title' in song
            assert 'artist_id' in song
            assert 'artist' in song
            assert 'status' in song


class TestDancesRoute:
    def test_dances_returns_list(self, client):
        """Test that /api/dances returns a list of dances."""
        response = client.get('/api/dances')
        assert response.status_code == 200
        dances = response.json
        assert isinstance(dances, list)
        assert len(dances) == 4

    def test_dances_have_required_fields(self, client):
        """Test that each dance has required fields."""
        response = client.get('/api/dances')
        dances = response.json
        for dance in dances:
            assert 'id' in dance
            assert 'song_id' in dance
            assert 'song' in dance
            assert 'status' in dance

    def test_dance_statuses_match_seed_data(self, client):
        """Test that dance statuses match seeded data."""
        response = client.get('/api/dances')
        dances = response.json
        status_map = {dance['song']: dance['status'] for dance in dances}
        expected_statuses = {
            'Wave': 'to do',
            'Butter': 'needs review',
            'Eenie Meenie': 'done',
            'Starmine': 'done'
        }
        assert status_map == expected_statuses