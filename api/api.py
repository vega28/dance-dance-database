import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name}

class Song(db.Model):
    __tablename__ = 'songs'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'), nullable=False)
    # TODO: make status an enum
    status: Mapped[str] = mapped_column(String(50), default='to do')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist_id': self.artist_id,
            'status': self.status
        }


# routes
@app.route('/api/hello', methods=['GET'])
def get_data():
    return {'message': 'hello from flask!'}

@app.route('/api/songs', methods=['GET'])
def get_songs():
    songs = [
        {'id': 1, 'title': 'Wave', 'artist': 'ATEEZ', 'status': 'to do'},
        {'id': 2, 'title': 'Butter', 'artist': 'BTS', 'status': 'needs review'},
        {'id': 3, 'title': 'Eenie Meenie', 'artist': 'Chungha', 'status': 'done'},
        {'id': 4, 'title': 'Starmine', 'artist': 'Da-Ice', 'status': 'done'},
        ]
    return songs


# ----------------------------------
if __name__ == "__main__":
    with app.app_context():
        try:
            db.session.execute(db.text('SELECT 1'))
            print("✓ Database connection successful!")
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
    app.run()