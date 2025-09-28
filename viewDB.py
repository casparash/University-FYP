import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("C:/Uni/CS3072/FYP/exercises_sports.db")  # Ensure this matches your database file
cursor = conn.cursor()

# Fetch all rows from the table
cursor.execute("SELECT * FROM exercises")  # Ensure this matches your table name
rows = cursor.fetchall()

# Check if the table is empty
if not rows:
    print("No data found in the table.")
else:
    # Print each row
    for row in rows:
        print(row)

# Fetch all rows from the table
cursor.execute("SELECT * FROM sports")  # Ensure this matches your table name
rows = cursor.fetchall()

# Check if the table is empty
if not rows:
    print("No data found in the table.")
else:
    # Print each row
    for row in rows:
        print(row)

# Fetch all rows from the table
cursor.execute("SELECT * FROM people")  # Ensure this matches your table name
rows = cursor.fetchall()

# Check if the table is empty
if not rows:
    print("No data found in the table.")
else:
    # Print each row
    for row in rows:
        print(row)

# Close the connection
conn.close()
