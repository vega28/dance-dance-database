"""Tests for database models."""
import pytest
from sqlalchemy.exc import IntegrityError


class TestArtistModel:
    def test_create_artist(self, app_context):
        """Test creating an artist."""
        from api.api import Artist, db
        
        artist = Artist(name='Test Artist')
        db.session.add(artist)
        db.session.commit()
        
        assert artist.id is not None
        assert artist.name == 'Test Artist'

    def test_artist_unique_constraint(self, app_context):
        """Test that artist names must be unique."""
        from api.api import Artist, db
        
        artist1 = Artist(name='Duplicate Name')
        db.session.add(artist1)
        db.session.commit()
        
        artist2 = Artist(name='Duplicate Name')
        db.session.add(artist2)
        
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_artist_to_dict(self, app_context):
        """Test Artist.to_dict() method."""
        from api.api import Artist, db
        
        artist = Artist(name='Test Artist')
        db.session.add(artist)
        db.session.commit()
        
        artist_dict = artist.to_dict()
        assert artist_dict['id'] == artist.id
        assert artist_dict['name'] == 'Test Artist'

    def test_query_artist_by_name(self, app_context):
        """Test querying artist by name."""
        from api.api import Artist, db
        
        artist = Artist(name='Query Test')
        db.session.add(artist)
        db.session.commit()
        
        found = Artist.query.filter_by(name='Query Test').first()
        assert found is not None
        assert found.name == 'Query Test'

    def test_artist_requires_name(self, app_context):
        """Test that artist name is required."""
        from api.api import Artist, db
        
        artist = Artist(name=None)
        db.session.add(artist)
        
        with pytest.raises(IntegrityError):
            db.session.commit()


class TestSongModel:
    def test_create_song(self, app_context):
        """Test creating a song."""
        from api.api import Artist, Song, db
        
        artist = Artist(name='Test Artist')
        db.session.add(artist)
        db.session.commit()
        
        song = Song(title='Test Song', artist_id=artist.id)
        db.session.add(song)
        db.session.commit()
        
        assert song.id is not None
        assert song.title == 'Test Song'
        assert song.artist_id == artist.id
        assert song.status == 'to do'  # default value

    def test_song_default_status(self, app_context):
        """Test that song status defaults to 'to do'."""
        from api.api import Artist, Song, db
        
        artist = Artist(name='Status Test Artist')
        db.session.add(artist)
        db.session.commit()
        
        song = Song(title='Status Test Song', artist_id=artist.id)
        db.session.add(song)
        db.session.commit()
        
        assert song.status == 'to do'

    def test_song_with_custom_status(self, app_context):
        """Test creating a song with a custom status."""
        from api.api import Artist, Song, db
        
        artist = Artist(name='Custom Status Artist')
        db.session.add(artist)
        db.session.commit()
        
        song = Song(title='Custom Status Song', artist_id=artist.id, status='done')
        db.session.add(song)
        db.session.commit()
        
        assert song.status == 'done'

    def test_song_to_dict(self, app_context):
        """Test Song.to_dict() method."""
        from api.api import Artist, Song, db
        
        artist = Artist(name='Dict Test Artist')
        db.session.add(artist)
        db.session.commit()
        
        song = Song(title='Dict Test Song', artist_id=artist.id, status='needs review')
        db.session.add(song)
        db.session.commit()
        
        song_dict = song.to_dict()
        assert song_dict['id'] == song.id
        assert song_dict['title'] == 'Dict Test Song'
        assert song_dict['artist_id'] == artist.id
        assert song_dict['status'] == 'needs review'

    def test_song_requires_title(self, app_context):
        """Test that song title is required."""
        from api.api import Artist, Song, db
        
        artist = Artist(name='Required Title Artist')
        db.session.add(artist)
        db.session.commit()
        
        song = Song(title=None, artist_id=artist.id)
        db.session.add(song)
        
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_song_requires_artist_id(self, app_context):
        """Test that song artist_id is required."""
        from api.api import Song, db
        
        song = Song(title='Orphan Song', artist_id=None)
        db.session.add(song)
        
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_song_artist_foreign_key(self, app_context):
        """Test that invalid artist_id raises error."""
        from api.api import Song, db
        
        song = Song(title='Invalid Artist Song', artist_id=9999)
        db.session.add(song)
        
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_query_songs_by_artist(self, app_context):
        """Test querying songs by artist."""
        from api.api import Artist, Song, db
        
        artist = Artist(name='Query Songs Artist')
        db.session.add(artist)
        db.session.commit()
        
        song1 = Song(title='Song 1', artist_id=artist.id)
        song2 = Song(title='Song 2', artist_id=artist.id)
        db.session.add_all([song1, song2])
        db.session.commit()
        
        songs = Song.query.filter_by(artist_id=artist.id).all()
        assert len(songs) == 2
        assert all(s.artist_id == artist.id for s in songs)
