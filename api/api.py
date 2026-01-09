import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import URL, ForeignKey, String

load_dotenv()


# database setup
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db_uri = URL.create(
    "postgresql+psycopg2",
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
)


# api setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.init_app(app)
CORS(app)
migrate = Migrate(app, db)


# models
class Artist(db.Model):
    __tablename__ = 'artists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    # relationships
    songs: Mapped[list['Song']] = relationship('Song', back_populates='artist', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 
            'name': self.name,
            'songs': [song.title for song in self.songs] if self.songs else []
            }

class Song(db.Model):
    __tablename__ = 'songs'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'), nullable=False)
    # TODO: make status an enum
    status: Mapped[str] = mapped_column(String(50), default='to do')
    
    # relationships
    artist: Mapped['Artist'] = relationship('Artist', back_populates='songs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist.name,
            'artist_id': self.artist_id,
            'status': self.status
        }


# routes
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


# ----------------------------------
# Register CLI commands (import lazily to avoid circular import issues)
def _register_cli_commands(app):
    try:
        from api.seed import seed
        app.cli.add_command(seed)
    except Exception:
        # don't break imports if seed or its dependencies aren't available
        # FIXME: set up seeding properly
        print("⚠️ Could not register CLI commands")
        pass


# register at import time so `flask --app api.api ...` sees the command
_register_cli_commands(app)

if __name__ == "__main__":
    with app.app_context():
        try:
            db.session.execute(db.text('SELECT 1'))
            print("✓ Database connection successful!")
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
    app.run()
