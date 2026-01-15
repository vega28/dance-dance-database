import pytest
import os
from api.api import create_app, db


@pytest.fixture
def client():
    """Create a test client with a PostgreSQL test database."""
    app = create_app(test=True)

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


# @pytest.fixture
# def seed_db(app_context):
#     """Seed the test database with sample data."""
#     from api.api import Artist, Song
    
#     # Create sample artists
#     artists_data = [
#         {'name': 'ATEEZ'},
#         {'name': 'BTS'},
#         {'name': 'Chungha'},
#         {'name': 'Da-Ice'},
#     ]
    
#     artists = []
#     for artist_data in artists_data:
#         artist = Artist(name=artist_data['name'])
#         artists.append(artist)
#         db.session.add(artist)
    
#     db.session.commit()
    
#     # Create sample songs
#     songs_data = [
#         {'title': 'Wave', 'artist_name': 'ATEEZ', 'status': 'to do'},
#         {'title': 'Butter', 'artist_name': 'BTS', 'status': 'needs review'},
#         {'title': 'Eenie Meenie', 'artist_name': 'Chungha', 'status': 'done'},
#         {'title': 'Starmine', 'artist_name': 'Da-Ice', 'status': 'done'},
#     ]
    
#     for song_data in songs_data:
#         artist = Artist.query.filter_by(name=song_data['artist_name']).first()
#         if artist:
#             song = Song(
#                 title=song_data['title'],
#                 artist_id=artist.id,
#                 status=song_data['status']
#             )
#             db.session.add(song)
    
#     db.session.commit()
#     yield
    
#     # Clean up
#     db.session.query(Song).delete()
#     db.session.query(Artist).delete()
#     db.session.commit()
