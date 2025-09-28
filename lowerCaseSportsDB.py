import sqlite3

# Connect to the database
conn = sqlite3.connect("exercises_sports.db")
cursor = conn.cursor()

# Update the 'sport' column to make all entries lowercase
cursor.execute("UPDATE sports SET sport = LOWER(sport)")

# Commit changes
conn.commit()

# Check if the update was successful by fetching the data
cursor.execute("SELECT sport FROM sports")
rows = cursor.fetchall()

for row in rows:
    print(row[0])  # Print each sport name in lowercase

# Close the connection
conn.close()