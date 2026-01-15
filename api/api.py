import os
from flask import Flask, app
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import URL
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
    from api.models import Artist, Song
    app = Flask(__name__)    
    app.config['TESTING'] = True if test else False
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri(test)
    db.init_app(app)
    CORS(app)
    migrate = Migrate(app, db)

    # routes ----------------------------------
    @app.route('/api/hello', methods=['GET'])
    def get_data():
        return {'message': 'hello from flask!'}

    @app.route('/api/artists', methods=['GET'])
    def get_artists():
        artists = [artist.to_dict() for artist in Artist.query.all()]
        return artists

    @app.route('/api/songs', methods=['GET'])
    def get_songs():
        songs = [song.to_dict() for song in Song.query.all()]
        return songs

    return app

# ----------------------------------

if __name__ == "__main__":
    from api.seed import seed
    app = create_app()
    seed()
    with app.app_context():
        try:
            db.session.execute(db.text('SELECT 1'))
            logger.info("✓ Database connection successful!")
        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
    app.run()
