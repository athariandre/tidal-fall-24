from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import numpy as np
from scipy.spatial import distance

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/databases/tempmerge.db')
    conn.row_factory = sqlite3.Row
    return conn


def find_nearest_k_vectors(vectors, target_vector, k):
    distances = distance.cdist([target_vector], vectors, 'euclidean')[0]
    nearest_k_indices = np.argsort(distances)[:k]
    return nearest_k_indices

def get_song():
    query_string = request.args.get('query')
    if not query_string:
        return jsonify({'error': 'No query string provided'}), 400

    try:
        song_title, artist_name = query_string.split(' by ')
    except ValueError:
        return jsonify({'error': 'Invalid query format. Use "song_title by artist_name"'}), 400

    conn = get_db_connection()
    song = conn.execute('SELECT * FROM merged_songs WHERE song_title = ? AND artist_name = ?', (song_title, artist_name)).fetchone()
    conn.close()

    if song is None:
        return jsonify({'error': 'Song not found'}), 404

    return jsonify(dict(song))

@app.route('/similar_songs', methods=['POST'])
def get_similar_songs():
    query_string = request.json['query']
    n = request.json['n']

    if not query_string:
        return jsonify({'error': 'No query string provided'}), 400
    if not n:
        return jsonify({'error': 'No number of similar songs provided'}), 400

    try:
        song_title, artist_name = query_string.split(' by ')
    except ValueError:
        return jsonify({'error': 'Invalid query format. Use "song_title by artist_name"'}), 400

    conn = get_db_connection()
    song = conn.execute('SELECT * FROM merged_songs WHERE song_title = ? AND artist_name = ?', (song_title, artist_name)).fetchone()
    
    if song is None:
        conn.close()
        return jsonify({'error': 'Song not found'}), 404

    # Assuming you have a 'features' column in your 'songs' table that stores the 17-dimensional feature vector
    # Construct the target feature vector using the specified columns
    target_vector = np.array([
        song['danceability'], song['acousticness'], song['instrumentalness'], song['liveness'],
        song['speechiness'], song['valence'], song['zcr'], song['spectral_contrast_mean'],
        song['chroma_mean'], song['mfccs_mean'], song['spectral_contrast_std'], song['chroma_std'], song['mfccs_std']
    ])
    
    # Fetch all other songs from the database
    all_songs = conn.execute('SELECT * FROM merged_songs WHERE song_title != ? AND artist_name != ?', (song_title, artist_name)).fetchall()
    conn.close()

    # Extract feature vectors from all songs
    vectors = np.array([
        [
            song['danceability'], song['acousticness'], song['instrumentalness'], song['liveness'],
            song['speechiness'], song['valence'], song['zcr'], song['spectral_contrast_mean'],
            song['chroma_mean'], song['mfccs_mean'], song['spectral_contrast_std'], song['chroma_std'], song['mfccs_std']
        ] for song in all_songs
    ])
    # Find the indices of the nearest k vectors
    nearest_k_indices = find_nearest_k_vectors(vectors, target_vector, n)
    # Get the similar songs using the indices
    similar_songs = [all_songs[i] for i in nearest_k_indices]

    # Include the original song in the response
    original_song = dict(song)
    similar_songs_list = [original_song] + [dict(row) for row in similar_songs]
    
    # Return the list of songs as a JSON response
    return jsonify(similar_songs_list)

# Add the route to the Flask app
app.route('/similar_songs', methods=['GET'])(get_similar_songs)


if __name__ == '__main__':
    app.run(debug=True)