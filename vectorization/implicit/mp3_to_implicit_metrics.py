import librosa
import os
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/databases/spotify_implicit.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS song_vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song_title TEXT,
        artist_name TEXT,
        mfccs TEXT,
        chroma TEXT,
        spectral_contrast TEXT,
        tempo REAL,
        zcr REAL
    )
''')

audio_filenames = [os.path.join(directory, filename) for directory, _, files in os.walk('/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/audio_files') for filename in files if filename.endswith('.mp3')]
cnt = 1
for filename in audio_filenames:
    y, sr = librosa.load(filename)
    

    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    tempo = librosa.beat.tempo(y=y, sr=sr)[0]
    zcr = librosa.feature.zero_crossing_rate(y)

    cleaned = filename.replace("/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/audio_files/", "")
    cleaned = cleaned.replace(".mp3", "")
    print(f"{cleaned} = {cnt}")
    try:
        artist, song_name = cleaned.split(" - ")
    except:
        continue


    
    cnt+=1

    # Insert song vector into the database
    # c.execute('''
    #     INSERT INTO song_vectors (song_title, artist_name, mfccs, chroma, spectral_contrast, tempo, zcr)
    #     VALUES (?, ?, ?, ?, ?, ?, ?)
    # ''', (
    #     song_name,
    #     artist,
    #     ','.join(map(str, mfccs.mean(axis=1).tolist())),
    #     ','.join(map(str, chroma.mean(axis=1).tolist())),
    #     ','.join(map(str, spectral_contrast.mean(axis=1).tolist())),
    #     tempo,
    #     zcr.mean().tolist()
    # ))

# Commit the transaction and close the connection
print("done")
conn.commit()
conn.close()
