import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL

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

# define routes
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