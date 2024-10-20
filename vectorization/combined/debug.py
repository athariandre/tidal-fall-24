import sqlite3
import pandas as pd


# Fetch and print all rows from the table for debugging
df_updated = pd.read_sql_query("SELECT * FROM song_vectors", merged)
print(df_updated)

# Close the database connection
conn_implicit.close()
