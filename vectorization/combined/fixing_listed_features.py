import pandas as pd
import numpy as np
import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/databases/tempmerge.db')

# Load your merged database
df = pd.read_sql_query('SELECT * FROM merged_songs', conn)

# Function to convert string representation of list to numpy array
def str_to_array(s):
    try:
        return np.array(eval(s, {"__builtins__": None}, {}))
    except:
        return np.array([])

# List of columns to process
columns_to_process = ['spectral_contrast', 'chroma', 'mfccs']

for col in columns_to_process:
    # Convert the string representation of lists to numpy arrays
    df[col] = df[col].apply(str_to_array)
    
    # Calculate mean and standard deviation
    df[f'{col}_mean'] = df[col].apply(np.mean)
    df[f'{col}_std'] = df[col].apply(np.std)

# Save the updated dataframe back to the SQLite database
# Create a new table with the updated schema
# Add new columns to the existing table
for col in [f'{col}_mean' for col in columns_to_process] + [f'{col}_std' for col in columns_to_process]:
    conn.execute(f'ALTER TABLE merged_songs ADD COLUMN {col} REAL')

# Update the existing table with the new data
for index, row in df.iterrows():
    update_query = f"""
    UPDATE merged_songs
    SET {', '.join([f"{col} = ?" for col in [f'{col}_mean' for col in columns_to_process] + [f'{col}_std' for col in columns_to_process]])}
    WHERE id = ?
    """
    conn.execute(update_query, tuple(row[[f'{col}_mean' for col in columns_to_process] + [f'{col}_std' for col in columns_to_process]]) + (row['id'],))

# Commit the changes
conn.commit()

# Close the connection
conn.close()