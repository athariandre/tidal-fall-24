import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sqlite3
import time
import os

# Replace with your Spotify API credentials
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

# Scope to access user's playlists
scope = 'playlist-read-private'

auth_manager = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope)

# Create Spotify object using the authenticated token
sp = spotipy.Spotify(auth_manager=auth_manager)

# Replace with your playlist ID
playlist_id = '4mPodK6ifH2VKsXj9a5JBs'

# Fetch the playlist tracks
playlist = sp.playlist_tracks(playlist_id)

count = 0 #count tracks processed regardless of validity
limit = 100 # Spotify API limit for tracks per request, prevents rate limiting
offset = 0 # Pagination offset

# Ensure we have valid tracks before accessing them
track_ids = []
track_names = []

while True:
    try:
        # Fetch playlist tracks with pagination
        playlist = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
        
        # Process tracks
        for track in playlist['items']:
            count += 1
            if track['track'] is not None and track['track']['id'] is not None:  # Ensure valid track
                track_ids.append(track['track']['id'])
                track_names.append(track['track']['name'])
        
        # If fewer than 100 items were returned, we've reached the end
        if len(playlist['items']) < limit:
            break

        # Move to the next set of 100 tracks
        offset += limit

        # Add a delay to avoid hitting the rate limit
        time.sleep(1) 

    except spotipy.SpotifyException as e:
        print(f"Error fetching tracks: {e}")
        time.sleep(5)  # Wait and retry in case of API issues


# Fetch audio features for each valid track
# Function to fetch audio features in batches with retry logic
def fetch_audio_features_with_retry(track_ids, sp, batch_size=100):
    audio_features = []
    for i in range(0, len(track_ids), batch_size):
        batch = track_ids[i:i + batch_size]  # Get batch of track IDs
        
        retries = 3
        while retries > 0:
            try:
                # Fetch audio features for the batch
                features = sp.audio_features(batch)
                audio_features.extend(features)
                break  # Exit retry loop if successful
            except spotipy.SpotifyException as e:
                print(f"Error fetching audio features: {e}")
                retries -= 1
                time.sleep(5)  # Delay before retrying
                if retries == 0:
                    print(f"Failed after retries for batch: {batch}")
    
    return audio_features

if track_ids:  # Check if track_ids list is not empty
    audio_features = fetch_audio_features_with_retry(track_ids, sp)

    # Extract relevant features for each song and print them alongside the track name
    for idx, features in enumerate(audio_features):
        if features:  # Ensure features are not None
            print(f"{track_names[idx]}")
            print(f"  Danceability: {features['danceability']}")
            print(f"  Acousticness: {features['acousticness']}")
            print(f"  Instrumentalness: {features['instrumentalness']}")
            print(f"  Liveness: {features['liveness']}")
            print(f"  Mode: {features['mode']}")
            print(f"  Speechiness: {features['speechiness']}")
            print(f"  Tempo: {features['tempo']}\n")

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('spotify_tracks.db')
cursor = conn.cursor()

# Create a table for storing the track data
cursor.execute('''
CREATE TABLE IF NOT EXISTS tracks (
    song_title TEXT,
    danceability REAL,
    acousticness REAL,
    instrumentalness REAL,
    liveness REAL,
    mode INTEGER,
    speechiness REAL,
    tempo REAL
)
''')
tracks = []
for idx, features in enumerate(audio_features):
        if features is not None:  # Check for None audio features
            track_data = (
                track_names[idx], 
                features['danceability'], 
                features['acousticness'], 
                features['instrumentalness'], 
                features['liveness'], 
                features['mode'], 
                features['speechiness'], 
                features['tempo']
            )
            tracks.append(track_data)

# Insert track data into the table
cursor.executemany('''
INSERT INTO tracks (song_title, danceability, acousticness, instrumentalness, liveness, mode, speechiness, tempo)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', tracks)

# Commit the transaction
conn.commit()

# Fetch and display the inserted data to verify
cursor.execute('SELECT * FROM tracks')
rows = cursor.fetchall()
print(len(rows))
for row in rows:
    print(row)

conn.close()
