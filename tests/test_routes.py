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


class TestArtistDetailRoute:
    def test_artist_detail_returns_artist(self, client):
        """Test that /api/artists/<artist_id> returns the correct artist."""
        response = client.get('/api/artists/1')
        assert response.status_code == 200
        artist = response.json
        assert artist['id'] == 1
        assert artist['name'] == 'ATEEZ'
        assert isinstance(artist['songs'], list)

    def test_artist_detail_invalid_id(self, client):
        """Test that /api/artists/<artist_id> returns 404 for invalid ID."""
        response = client.get('/api/artists/999')
        assert response.status_code == 404
        assert response.json['error'] == 'Artist not found'


class TestAddArtistRoute:
    def test_add_artist_creates_artist(self, client):
        """Test that POST /api/artists creates a new artist."""
        new_artist = {'name': 'New Artist'}
        response = client.post('/api/artists', json=new_artist)
        assert response.status_code == 201
        artist = response.json
        assert artist['name'] == 'New Artist'
        assert 'id' in artist
        assert artist['songs'] == []

    def test_add_artist_missing_name(self, client):
        """Test that POST /api/artists with missing name returns 400."""
        new_artist = {}
        response = client.post('/api/artists', json=new_artist)
        assert response.status_code == 400
        assert response.json['error'] == 'Missing field: name'


class TestEditArtistRoute:
    def test_edit_artist_updates_artist(self, client):
        """Test that PUT /api/artists/<artist_id> updates an existing artist."""
        updated_data = {'name': 'Updated Artist Name'}
        response = client.put('/api/artists/1', json=updated_data)
        assert response.status_code == 200
        artist = response.json
        assert artist['name'] == 'Updated Artist Name'

    def test_edit_artist_invalid_id(self, client):
        """Test that PUT /api/artists/<artist_id> with invalid ID returns 404."""
        updated_data = {'name': 'Nonexistent Artist'}
        response = client.put('/api/artists/999', json=updated_data)
        assert response.status_code == 404
        assert response.json['error'] == 'Artist not found'


class TestDeleteArtistRoute:
    def test_delete_artist_removes_artist(self, client):
        """Test that DELETE /api/artists/<artist_id> removes the artist."""
        response = client.delete('/api/artists/1')
        assert response.status_code == 200
        assert response.json['message'] == 'Artist deleted successfully'

        # Verify artist is actually deleted
        get_response = client.get('/api/artists/1')
        assert get_response.status_code == 404

    def test_delete_artist_invalid_id(self, client):
        """Test that DELETE /api/artists/<artist_id> with invalid ID returns 404."""
        response = client.delete('/api/artists/999')
        assert response.status_code == 404
        assert 'error' in response.json
        assert response.json['error'] == 'Artist not found'


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


class TestSongDetailRoute:
    def test_song_detail_returns_song(self, client):
        """Test that /api/songs/<song_id> returns the correct song."""
        response = client.get('/api/songs/1')
        assert response.status_code == 200
        song = response.json
        assert song['id'] == 1
        assert song['title'] == 'Wave'
        assert song['artist'] == 'ATEEZ'
        assert song['status'] == 'to do'

    def test_song_detail_invalid_id(self, client):
        """Test that /api/songs/<song_id> returns 404 for invalid ID."""
        response = client.get('/api/songs/999')
        assert response.status_code == 404
        assert response.json['error'] == 'Song not found'


class TestAddSongRoute:
    def test_add_song_creates_song(self, client):
        """Test that POST /api/songs creates a new song."""
        new_song = {
            'title': 'New Song',
            'artist_name': 'BTS'
        }
        response = client.post('/api/songs', json=new_song)
        assert response.status_code == 201
        song = response.json
        assert song['title'] == 'New Song'
        assert song['artist'] == 'BTS'
        assert song['status'] is None  # No dance yet

    def test_add_song_missing_fields(self, client):
        """Test that POST /api/songs with missing fields returns 400."""
        new_song = {
            'title': 'Song of Incomplete Data'
            # Missing artist_name
        }
        response = client.post('/api/songs', json=new_song)
        assert response.status_code == 400
        assert response.json['error'] == 'Missing field: artist_name'


class TestEditSongRoute:
    def test_edit_song_updates_song(self, client):
        """Test that PUT /api/songs/<song_id> updates an existing song."""
        updated_data = {
            'title': 'Updated Wave',
            'artist_name': 'ATEEZ'
        }
        response = client.put('/api/songs/1', json=updated_data)
        assert response.status_code == 200
        song = response.json
        assert song['title'] == 'Updated Wave'
        assert song['artist'] == 'ATEEZ'
        
    def test_edit_song_invalid_id(self, client):
        """Test that PUT /api/songs/<song_id> with invalid ID returns 404."""
        updated_data = {
            'title': 'Nonexistent Song',
            'artist_name': 'ATEEZ'
        }
        response = client.put('/api/songs/999', json=updated_data)
        assert response.status_code == 404
        assert 'error' in response.json


class TestDeleteSongRoute:
    def test_delete_song_removes_song(self, client):
        """Test that DELETE /api/songs/<song_id> removes the song."""
        response = client.delete('/api/songs/1')
        assert response.status_code == 200
        assert response.json['message'] == 'Song deleted successfully'

        # Verify song is actually deleted
        get_response = client.get('/api/songs/1')
        assert get_response.status_code == 404

    def test_delete_song_invalid_id(self, client):
        """Test that DELETE /api/songs/<song_id> with invalid ID returns 404."""
        response = client.delete('/api/songs/999')
        assert response.status_code == 404
        assert 'error' in response.json
        assert response.json['error'] == 'Song not found'


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


class TestDanceDetailRoute:
    def test_dance_detail_returns_dance(self, client):
        """Test that /api/dances/<dance_id> returns the correct dance."""
        response = client.get('/api/dances/1')
        assert response.status_code == 200
        dance = response.json
        assert dance['id'] == 1
        assert dance['song'] == 'Wave'
        assert dance['status'] == 'to do'
    
    def test_dance_detail_invalid_id(self, client):
        """Test that /api/dances/<dance_id> returns 404 for invalid ID."""
        response = client.get('/api/dances/999')
        assert response.status_code == 404
        assert response.json['error'] == 'Dance not found'


class TestAddDanceRoute:
    def test_add_dance_creates_dance(self, client):
        """Test that POST /api/dances creates a new dance."""
        from api.api import db
        from api.models import Song
        song = Song(title='Test Song', artist_id=2)
        db.session.add(song)
        db.session.commit()
        new_dance = {
            'song_id': song.id,
            'status': 'to do'
        }
        response = client.post('/api/dances', json=new_dance)
        assert response.status_code == 201
        dance = response.json
        assert dance['song'] == 'Test Song'
        assert dance['status'] == 'to do'


class TestEditDanceRoute:
    def test_edit_dance_updates_dance(self, client):
        """Test that PUT /api/dances/<dance_id> updates an existing dance."""
        updated_data = {
            'status': 'done'
        }
        response = client.put('/api/dances/1', json=updated_data)
        assert response.status_code == 200
        dance = response.json
        assert dance['status'] == 'done'
    
    def test_edit_dance_invalid_id(self, client):
        """Test that PUT /api/dances/<dance_id> with invalid ID returns 404."""
        updated_data = {
            'status': 'done'
        }
        response = client.put('/api/dances/999', json=updated_data)
        assert response.status_code == 404
        assert 'error' in response.json


class TestDeleteDanceRoute:
    def test_delete_dance_removes_dance(self, client):
        """Test that DELETE /api/dances/<dance_id> removes the dance."""
        response = client.delete('/api/dances/1')
        assert response.status_code == 200
        assert response.json['message'] == 'Dance deleted successfully'

        # Verify dance is actually deleted
        get_response = client.get('/api/dances/1')
        assert get_response.status_code == 404
    
    def test_delete_dance_invalid_id(self, client):
        """Test that DELETE /api/dances/<dance_id> with invalid ID returns 404."""
        response = client.delete('/api/dances/999')
        assert response.status_code == 404
        assert 'error' in response.json