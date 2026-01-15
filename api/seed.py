"""Database seeding command."""
from . import db, logger

def seed():
    """Seed the database with initial data."""
    # import models lazily to avoid circular imports when registering CLI
    from api.models import Artist, Song

    # Check if data already exists
    if Artist.query.first():
        logger.warning("Database already seeded. Skipping...")
        return

    # Create artists
    artists_data = [
        {'name': 'ATEEZ'},
        {'name': 'BTS'},
        {'name': 'Chungha'},
        {'name': 'Da-Ice'},
    ]
    
    artists = []
    for artist_data in artists_data:
        artist = Artist(name=artist_data['name'])
        artists.append(artist)
        db.session.add(artist)
    
    db.session.commit()
    logger.info(f"✓ Created {len(artists)} artists")
    
    # Create songs
    songs_data = [
        {'title': 'Wave', 'artist_name': 'ATEEZ', 'status': 'to do'},
        {'title': 'Butter', 'artist_name': 'BTS', 'status': 'needs review'},
        {'title': 'Eenie Meenie', 'artist_name': 'Chungha', 'status': 'done'},
        {'title': 'Starmine', 'artist_name': 'Da-Ice', 'status': 'done'},
    ]
    
    songs = []
    for song_data in songs_data:
        artist = Artist.query.filter_by(name=song_data['artist_name']).first()
        if artist:
            song = Song(
                title=song_data['title'],
                artist_id=artist.id,
                status=song_data['status']
            )
            songs.append(song)
            db.session.add(song)
    
    db.session.commit()
    logger.info(f"✓ Created {len(songs)} songs")
    logger.info("✓ Database seeded successfully!")
