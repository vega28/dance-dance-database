import time
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/hello', methods=['GET'])
def get_data():
    return {'message': 'hello from flask!'}

@app.route('/api/time', methods=['GET'])
def get_time():
    return { 'time': time.time()}

@app.route('/api/songs', methods=['GET'])
def get_songs():
    songs = [{'id': 1, 'title': 'Wave', 'artist': 'ATEEZ'},
             {'id': 2, 'title': 'Butter', 'artist': 'BTS'},
             {'id': 3, 'title': 'Eenie Meenie', 'artist': 'Chungha'}]
    return songs

# ----------------------------------
if __name__ == "__main__":
    app.run()