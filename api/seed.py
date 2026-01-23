"""Database seeding command."""
from . import db, logger
from sqlalchemy import select

def seed():
    """Seed the database with initial data."""
    # import models lazily to avoid circular imports when registering CLI
    from api.models import Artist, Song, Dance

    # Check if data already exists
    if db.session.scalars(select(Artist)).first() is not None:
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
        {'title': 'Wave', 'artist_name': 'ATEEZ'},
        {'title': 'Butter', 'artist_name': 'BTS'},
        {'title': 'Eenie Meenie', 'artist_name': 'Chungha'},
        {'title': 'Starmine', 'artist_name': 'Da-Ice'},
    ]
    
    songs = []
    for song_data in songs_data:
        artist = db.session.scalars(select(Artist).where(Artist.name == song_data['artist_name'])).first()
        if artist:
            song = Song(
                title=song_data['title'],
                artist_id=artist.id,
            )
            songs.append(song)
            db.session.add(song)
    
    db.session.commit()
    logger.info(f"✓ Created {len(songs)} songs")

    # Create dances
    dances_data = [
        {'song_title': 'Wave', 'status': 'to do'},
        {'song_title': 'Butter', 'status': 'needs review'},
        {'song_title': 'Eenie Meenie', 'status': 'done'},
        {'song_title': 'Starmine', 'status': 'done'},
    ]
    dances = []
    for dance_data in dances_data:
        song = db.session.scalars(select(Song).where(Song.title == dance_data['song_title'])).first()
        if song:
            dance = Dance(
                song_id=song.id,
                status=dance_data['status']
            )
            dances.append(dance)
            db.session.add(dance)
    
    db.session.commit()
    logger.info(f"✓ Created {len(dances)} dances")

    logger.info("✓ Database seeded successfully!")
