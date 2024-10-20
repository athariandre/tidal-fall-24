import sqlite3
import pandas as pd

# Connect to the databases
conn_explicit = sqlite3.connect('/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/databases/spotify_explicit.db')
conn_implicit = sqlite3.connect('/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/databases/spotify_implicit.db')

# Read the tables into DataFrames
df_explicit = pd.read_sql_query("SELECT * FROM tracks", conn_explicit)
df_implicit = pd.read_sql_query("SELECT * FROM song_vectors", conn_implicit)

# Perform the center join on song_name and artist_name
merged_df = pd.merge(df_explicit, df_implicit, on=['song_title', 'artist_name'], how='inner')

# Close the database connections
conn_explicit.close()
conn_implicit.close()

# Save the merged DataFrame to a new SQLite database
conn_merged = sqlite3.connect('/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/databases/merged.db')
merged_df.to_sql('merged_songs', conn_merged, if_exists='replace', index=False)
conn_merged.close()

print(f"The merged database contains {len(merged_df)} records.")