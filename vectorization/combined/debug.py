import sqlite3
import pandas as pd

# Establish a connection to the SQLite database
conn_implicit = sqlite3.connect('/Users/andre/Projects/competition/tidal-fall-24/vectorization/data/databases/tempmerge.db')

# Fetch and print all column names from the table for debugging
cursor = conn_implicit.cursor()
cursor.execute("PRAGMA table_info(merged_songs)")
columns = [column[1] for column in cursor.fetchall()]
print("Column names:", columns)
print("len of columns:", len(columns))

# Fetch and print all rows where artist_name is 'cochise' from the table for debugging
df_updated = pd.read_sql_query("SELECT * FROM merged_songs WHERE artist_name = 'Cochise'", conn_implicit)
print(df_updated)

# Close the database connection
conn_implicit.close()
