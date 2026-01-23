import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import URL, select
from . import db, logger

def get_db_uri(test=False):
    """Construct the database URI from environment variables."""
    if test:
        # Use PostgreSQL test database
        db_uri = os.getenv('TEST_DATABASE_URI')
        if not db_uri:
            raise RuntimeError(
                "TEST_DATABASE_URI environment variable is not set. "
                "Please set it to a valid PostgreSQL test database URI before running tests."
            )
    else:
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port_raw = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')

        missing_db_vars = [
            var_name for var_name, value in [
                ('DB_USER', db_user),
                ('DB_PASSWORD', db_password),
                ('DB_HOST', db_host),
                ('DB_PORT', db_port_raw),
                ('DB_NAME', db_name),
            ]
            if value is None or value == ''
        ]

        if missing_db_vars:
            raise RuntimeError(
                f"Missing required database environment variable(s): {', '.join(missing_db_vars)}"
            )

        try:
            db_port = int(db_port_raw)
        except (TypeError, ValueError):
            raise RuntimeError("Invalid DB_PORT environment variable: must be an integer")

        db_uri = URL.create(
            "postgresql+psycopg2",
            username=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name,
        )
    return db_uri

def create_app(test=False):
    from api.models import Artist, Song, Dance
    app = Flask(__name__)    
    app.config['TESTING'] = test
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri(test)
    db.init_app(app)
    CORS(app)
    Migrate(app, db, compare_type=True)

    # RESTful routes ----------------------------------
    # TODO: improve error handling, validation, cascade effects, etc.
    
    # hello route
    @app.route('/api/hello', methods=['GET'])
    def get_data():
        return {'message': 'hello from flask!'}

    # artist routes
    @app.route('/api/artists', methods=['GET'])
    def get_artists():
        artist_collection = db.session.scalars(select(Artist)).all()
        artists = [artist.to_dict() for artist in artist_collection]
        return artists
    
    @app.route('/api/artists/<int:artist_id>', methods=['GET'])
    def get_artist(artist_id):
        artist = db.session.get(Artist, artist_id)
        if not artist:
            return jsonify({'error': 'Artist not found'}), 404
        return artist.to_dict()
    
    @app.route('/api/artists', methods=['POST'])
    def add_artist():
        try:
            data = request.json
            artist = Artist(name=data['name'])
            db.session.add(artist)
            db.session.commit()
            return jsonify(artist.to_dict()), 201
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error adding artist: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/artists/<int:artist_id>', methods=['PUT'])
    def edit_artist(artist_id):
        try:
            artist = db.session.get(Artist, artist_id)
            if not artist:
                return jsonify({'error': 'Artist not found'}), 404
            data = request.json
            if 'name' in data:
                artist.name = data['name']
            db.session.commit()
            return jsonify(artist.to_dict()), 200
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error updating artist: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/artists/<int:artist_id>', methods=['DELETE'])
    def delete_artist(artist_id):
        try:
            artist = db.session.get(Artist, artist_id)
            if not artist:
                return jsonify({'error': 'Artist not found'}), 404
            db.session.delete(artist)
            db.session.commit()
            return jsonify({'message': 'Artist deleted successfully'}), 200
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error deleting artist: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    # song routes
    @app.route('/api/songs', methods=['GET'])
    def get_songs():
        song_collection = db.session.scalars(select(Song)).all()
        songs = [song.to_dict() for song in song_collection]
        return songs
    
    @app.route('/api/songs/<int:song_id>', methods=['GET'])
    def get_song(song_id):
        song = db.session.get(Song, song_id)
        if not song:
            return jsonify({'error': 'Song not found'}), 404
        return song.to_dict()
    
    @app.route('/api/songs', methods=['POST'])
    def add_song():
        try:
            data = request.json
            artist = db.session.scalars(select(Artist).where(Artist.name == data['artist_name'])).first()
            if not artist:
                return jsonify({'error': 'Artist not found'}), 404
            song = Song(title=data['title'], artist_id=artist.id)
            db.session.add(song)
            db.session.commit()
            return jsonify(song.to_dict()), 201
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error adding song: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/songs', methods=['PUT'])
    # FIXME: required fields: song_id OR title + artist_name
    def edit_song():
        try:
            data = request.json
            if 'song_id' in data:
                song = db.session.get(Song, data['song_id'])
            else:
                artist = db.session.scalars(select(Artist).where(Artist.name == data['artist_name'])).first()
                if not artist:
                    return jsonify({'error': 'Artist not found'}), 404
                song = db.session.scalars(
                    select(Song).where(
                        Song.title == data['title'],
                        Song.artist_id == artist.id
                    )
                ).first()
            if not song:
                return jsonify({'error': 'Song not found'}), 404
            if 'title' in data:
                song.title = data['title']
            if 'artist_name' in data:
                artist = db.session.scalars(select(Artist).where(Artist.name == data['artist_name'])).first()
                if not artist:
                    return jsonify({'error': 'Artist not found'}), 404
                song.artist_id = artist.id
            db.session.commit()
            return jsonify(song.to_dict()), 200
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error updating song: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/songs/<int:song_id>', methods=['DELETE'])
    def delete_song(song_id):
        try:
            song = db.session.get(Song, song_id)
            if not song:
                return jsonify({'error': 'Song not found'}), 404
            db.session.delete(song)
            db.session.commit()
            return jsonify({'message': 'Song deleted successfully'}), 200
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error deleting song: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    # dance routes
    @app.route('/api/dances', methods=['GET'])
    def get_dances():
        dance_collection = db.session.scalars(select(Dance)).all()
        dances = [dance.to_dict() for dance in dance_collection]
        return dances

    @app.route('/api/dances/<int:dance_id>', methods=['GET'])
    def get_dance(dance_id):
        dance = db.session.get(Dance, dance_id)
        if not dance:
            return jsonify({'error': 'Dance not found'}), 404
        return dance.to_dict()

    @app.route('/api/dances', methods=['POST'])
    def add_dance():
        try:
            data = request.json
            song = db.session.get(Song, data['song_id'])
            if not song:
                return jsonify({'error': 'Song not found'}), 404
            status = data.get('status', 'to do')
            dance = Dance(song_id=song.id, status=status)
            db.session.add(dance)
            db.session.commit()
            return jsonify(dance.to_dict()), 201
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error adding dance: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/api/dances/<int:dance_id>', methods=['PUT'])
    def edit_dance(dance_id):
        try:
            dance = db.session.get(Dance, dance_id)
            if not dance:
                return jsonify({'error': 'Dance not found'}), 404
            data = request.json
            if 'status' in data:
                dance.status = data['status']
            db.session.commit()
            return jsonify(dance.to_dict()), 200
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error updating dance: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/api/dances/<int:dance_id>', methods=['DELETE'])
    def delete_dance(dance_id):
        try:
            dance = db.session.get(Dance, dance_id)
            if not dance:
                return jsonify({'error': 'Dance not found'}), 404
            db.session.delete(dance)
            db.session.commit()
            return jsonify({'message': 'Dance deleted successfully'}), 200
        except KeyError as e:
            return jsonify({'error': f'Missing field: {e.args[0]}'}), 400
        except Exception as e:
            logger.error(f"Error deleting dance: {e}")
            return jsonify({'error': 'Internal server error'}), 500    

    return app

# ----------------------------------

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        from api.seed import seed
        from sqlalchemy import text
        seed()
        try:
            db.session.execute(text('SELECT 1'))
            logger.info("✓ Database connection successful!")
        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
    app.run()
