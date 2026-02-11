"""Tests for database models."""
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select


class TestArtistModel:
    def test_create_artist(self, db_session):
        """Test creating an artist."""
        from api.models import Artist
        
        artist = Artist(name='Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        assert artist.id is not None
        assert artist.name == 'Test Artist'

    def test_artist_unique_constraint(self, db_session):
        """Test that artist names must be unique."""
        from api.models import Artist
        
        artist1 = Artist(name='Duplicate Name')
        db_session.add(artist1)
        db_session.commit()
        
        artist2 = Artist(name='Duplicate Name')
        db_session.add(artist2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_artist_to_dict(self, db_session):
        """Test Artist.to_dict() method."""
        from api.models import Artist
        
        artist = Artist(name='Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        artist_dict = artist.to_dict()
        assert artist_dict['id'] == artist.id
        assert artist_dict['name'] == 'Test Artist'
        assert artist_dict['songs'] == []

    def test_query_artist_by_name(self, db_session):
        """Test querying artist by name."""
        from api.models import Artist
        
        artist = Artist(name='Query Test')
        db_session.add(artist)
        db_session.commit()
        
        found = db_session.scalars(select(Artist).where(Artist.name == 'Query Test')).first()
        assert found is not None
        assert found.name == 'Query Test'

    def test_artist_requires_name(self, db_session):
        """Test that artist name is required."""
        from api.models import Artist
        
        artist = Artist(name=None)
        db_session.add(artist)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    # TODO: test relationship with songs


class TestSongModel:
    def test_create_song(self, db_session):
        """Test creating a song."""
        from api.models import Artist, Song
        
        artist = Artist(name='Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        song = Song(title='Test Song', artist_id=artist.id)
        db_session.add(song)
        db_session.commit()
        
        assert song.id is not None
        assert song.title == 'Test Song'
        assert song.artist_id == artist.id

    def test_song_to_dict(self, db_session):
        """Test Song.to_dict() method."""
        from api.models import Artist, Song, Dance
        
        artist = Artist(name='Dict Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        song = Song(title='Dict Test Song', artist_id=artist.id)
        db_session.add(song)
        db_session.commit()

        dance = Dance(song=song, status='needs review')
        db_session.add(dance)
        db_session.commit()
        
        song_dict = song.to_dict()
        assert song_dict['id'] == song.id
        assert song_dict['title'] == 'Dict Test Song'
        assert song_dict['artist'] == artist.name
        assert song_dict['artist_id'] == artist.id
        assert song_dict['status'] == 'needs review'

    def test_song_requires_title(self, db_session):
        """Test that song title is required."""
        from api.models import Artist, Song
        
        artist = Artist(name='Required Title Artist')
        db_session.add(artist)
        db_session.commit()
        
        song = Song(title=None, artist_id=artist.id)
        db_session.add(song)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_song_requires_artist_id(self, db_session):
        """Test that song artist_id is required."""
        from api.models import Song
        
        song = Song(title='Orphan Song', artist_id=None)
        db_session.add(song)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_song_artist_foreign_key(self, db_session):
        """Test that invalid artist_id raises error."""
        from api.models import Song
        
        song = Song(title='Invalid Artist Song', artist_id=9999)
        db_session.add(song)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_query_songs_by_artist(self, db_session):
        """Test querying songs by artist."""
        from api.models import Artist, Song
        
        artist = Artist(name='Query Songs Artist')
        db_session.add(artist)
        db_session.commit()
        
        song1 = Song(title='Song 1', artist_id=artist.id)
        song2 = Song(title='Song 2', artist_id=artist.id)
        db_session.add_all([song1, song2])
        db_session.commit()
        
        songs = db_session.scalars(select(Song).where(Song.artist_id == artist.id)).all()
        assert len(songs) == 2
        assert all(s.artist_id == artist.id for s in songs)


class TestDanceModel:
    def test_create_dance(self, db_session):
        """Test creating a dance."""
        from api.models import Artist, Song, Dance
        
        artist = Artist(name='Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        song = Song(title='Test Song', artist_id=artist.id)
        db_session.add(song)
        db_session.commit()
        
        dance = Dance(song=song, status='done')
        db_session.add(dance)
        db_session.commit()
        
        assert dance.id is not None
        assert dance.song == song
        assert dance.song_id == song.id
        assert dance.status == 'done'

    def test_dance_default_status(self, db_session):
        """Test that dance status defaults to 'to do'."""
        from api.models import Artist, Song, Dance
        
        artist = Artist(name='Status Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        song = Song(title='Status Test Song', artist_id=artist.id)
        db_session.add(song)
        db_session.commit()
        
        dance = Dance(song=song)
        db_session.add(dance)
        db_session.commit()
        
        assert dance.status == 'to do'

    @pytest.mark.skip(reason="Enum constraint not yet enforced at DB level")
    def test_dance_invalid_status(self, db_session):
        """Test that dance status must be a valid enum."""
        from api.models import Artist, Song, Dance
        
        artist = Artist(name='Status Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        song = Song(title='Status Test Song', artist_id=artist.id)
        db_session.add(song)
        db_session.commit()
        
        dance = Dance(song=song, status='oof')
        db_session.add(dance)

        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_dance_song_foreign_key(self, db_session):
        """Test that invalid song_id raises error."""
        from api.models import Dance
        dance = Dance(song_id=9999)
        db_session.add(dance)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    @pytest.mark.skip(reason="FIXME: run migrations properly in test setup!")
    def test_dance_unique_song_constraint(self, db_session):
        """Test that each song can have only one dance."""
        from api.models import Artist, Song, Dance
        
        artist = Artist(name='Unique Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        song = Song(title='Unique Test Song', artist_id=artist.id)
        db_session.add(song)
        db_session.commit()
        
        dance1 = Dance(song=song, status='to do')
        db_session.add(dance1)
        db_session.commit()
        
        dance2 = Dance(song=song, status='in progress')
        db_session.add(dance2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_dance_to_dict(self, db_session):
        """Test Dance.to_dict() method."""
        from api.models import Artist, Song, Dance
        
        artist = Artist(name='Dict Test Artist')
        db_session.add(artist)
        db_session.commit()
        
        song = Song(title='Dict Test Song', artist_id=artist.id)
        db_session.add(song)
        db_session.commit()

        dance = Dance(song=song, status='needs review')
        db_session.add(dance)
        db_session.commit()
        
        dance_dict = dance.to_dict()
        assert dance_dict['id'] == dance.id
        assert dance_dict['song'] == song.title
        assert dance_dict['song_id'] == song.id
        assert dance_dict['status'] == 'needs review'
