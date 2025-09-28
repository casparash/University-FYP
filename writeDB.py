import sqlite3
import pandas as pd
import os

# Load Excel file
excel_file = "C:/Uni/CS3072/FYP/Database Draft.xlsx"  # Change this to your file name
df = pd.read_excel(excel_file, sheet_name="Sheet5")  # Load the first sheet

print(f"File exists: {os.path.exists(excel_file)}")

print(df.head(10))  # Print first 10 rows
print(df.dtypes)  # Check data types

# Connect to a local database (creates file if it doesn't exist)
conn = sqlite3.connect("exercises_sports.db")

# Create a cursor object to interact with the database
cursor = conn.cursor()

#cursor.execute('''DROP TABLE IF EXISTS exercises;''')

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT,
        difficulty INTEGER,
        equipment TEXT,
        type TEXT,
        muscleGroups TEXT
    )
''')

# Insert data into SQLite
for _, row in df.iterrows():
    cursor.execute("INSERT INTO exercises (id, exercise, difficulty, equipment, type, muscleGroups) VALUES (?, ?, ?, ?, ?, ?)", 
                   (row["#"], row["Exercise"], row["Difficulty"], row["Equipment Needed"], row["Type"], row["Muscle Group(s)"]))
    
conn.commit()
    
df = pd.read_excel(excel_file, sheet_name="Sheet2")  # Load the second sheet

print(f"File exists: {os.path.exists(excel_file)}")

print(df.head(10))  # Print first 10 rows
print(df.dtypes)  # Check data types

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sport TEXT,
        anaerobic FLOAT,
        aerobic FLOAT,
        muscleGroups TEXT
    )
''')

# Insert data into SQLite
for _, row in df.iterrows():
    cursor.execute("INSERT INTO sports (id, sport, anaerobic, aerobic, muscleGroups) VALUES (?, ?, ?, ?, ?)", 
                   (row["#"], row["Sport"], row["Anaerobic (%)"], row["Aerobic (%)"], row["Top 3 Muscle Groups Used"]))
    
df = pd.read_excel(excel_file, sheet_name="Sheet4")  # Load the fourth sheet

print(f"File exists: {os.path.exists(excel_file)}")

print(df.head(10))  # Print first 10 rows
print(df.dtypes)  # Check data types

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        name TEXT PRIMARY KEY,
        age INTEGER,
        skill INTEGER,
        sessionNumber INTEGER,
        sessionLength INTEGER,
        sport TEXT
    )
''')

# Insert data into SQLite
for _, row in df.iterrows():
    cursor.execute("INSERT INTO people (name, age, skill, sessionNumber, sessionLength, sport) VALUES (?, ?, ?, ?, ?, ?)", 
                   (row["Name"], row["Age"], row["Skill"], row["Sessions per Week"], row["Session Length"], row["Sport"]))

# Commit and close connection
conn.commit()
conn.close()

