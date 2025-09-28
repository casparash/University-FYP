import sqlite3
import random
import pandas as pd

#Adds data to the people table
def insertPeopleData(name, age, skill, sessionNumber, sessionLength, sport):

    #Connect to the database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Add varibales to the people table
    cursor.execute("INSERT OR REPLACE INTO people (name, age, skill, sessionNumber, sessionLength, sport) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, age, skill, sessionNumber, sessionLength, sport))
    
    #Commit the changes
    conn.commit()

    #Close the connection
    conn.close()

#Gets all the data from the people table
def viewPeopleData():

    #Connect to the database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Get all the data from people table
    cursor.execute("SELECT * FROM people")

    #Save data to variable
    rows = cursor.fetchall()

    #Checks to see if any data in rows
    if not rows:
        print("No data found in the table.")

    #Close the connection
    conn.close()

    return rows

#Gets all sports from sports table
def getSports():

    #Connect to database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Gets all data from sport column in sports table
    cursor.execute("SELECT sport FROM sports")

    #Saves all sports and removes any {}
    sports = [row[0].strip("{}") for row in cursor.fetchall()]

    #Checks the variable has any data in it
    if not sports:
        print("No data found in the table.")
    
    #Close the connection
    conn.close()

    return sports

#Gets all exercise names from exercise table
def getExercises():

    #Connect to database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Gets all data from exercise column in exercises table
    cursor.execute("SELECT exercise FROM exercises")

    #Saves all exercises and removes any {}
    exercises = [row[0] for row in cursor.fetchall()]

    #Checks the variable has any data in it
    if not exercises:
        print("No data found in the table.")
    
    #Close the connection
    conn.close()

    return exercises

#Gets all muscle groups from exercise table
def getMuscleGroups():

    #Connect to database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Gets all data from muscleGroups column in exercises table
    cursor.execute("SELECT muscleGroups FROM exercises")

    #Saves all muscle groups
    muscleGroups = [row[0] for row in cursor.fetchall()]
    muscleGroups = list(dict.fromkeys(muscleGroups))

    #Checks the variable has any data in it
    if not muscleGroups:
        print("No data found in the table.")
    
    #Close the connection
    conn.close()

    return muscleGroups

#Gets all info on specific sport from sports table
def getSportSpecific(sport):

    #Connect to database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sports WHERE sport LIKE ?", ('%' + sport + '%',))

    result = cursor.fetchone()

    #Checks the variable has any data in it
    if not sport:
        print("No data found in the table.")
    
    #Close the connection
    conn.close()

    return result

#Gets all info on specific exercise from exercise table
def getExercisesSpecific(exercise):

    #Connect to database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM exercises WHERE exercise LIKE ?", ('%' + exercise + '%',))

    result = cursor.fetchone()

    #Checks the variable has any data in it
    if not result:
        print("No data found in the table.")
    
    #Close the connection
    conn.close()

    return result

#Gets all exercises that match the specific type from exercise table
def getExercisesType(type):

    #Connect to database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Gets all data from exercise column in exercises table
    cursor.execute("SELECT exercise FROM exercises WHERE type LIKE ?", ('%' + type + '%',))

    #Saves all exercises and removes any {}
    exercises = [row[0] for row in cursor.fetchall()]

    #Checks the variable has any data in it
    if not exercises:
        print("No data found in the table.")
    
    #Close the connection
    conn.close()

    return exercises

#Creates the testing table
def createTestingTable():

    #Connect to a local database (creates file if it doesn't exist)
    conn = sqlite3.connect("exercises_sports.db")

    #Create a cursor object to interact with the database
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS testing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm TEXT,
            completionTime FLOAT,
            fitness FLOAT,
            difficulty INTEGER,
            focus INTEGER,
            overallRating INTEGER,
            comments TEXT,
            plan TEXT,
            user TEXT
        )
    ''')
    #Commit and close connection
    conn.commit()
    conn.close()

#Add to testing table
def insertTestingData(algorithm, completionTime, fitness, difficulty, focus, overallRating, comments, plan, user):

    #Connect to the database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Add varibales to the people table
    cursor.execute("INSERT OR REPLACE INTO testing (algorithm, completionTime, fitness, difficulty, focus, overallRating, comments, plan, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (algorithm, completionTime, fitness, difficulty, focus, overallRating, comments, plan, user))
    
    #Commit the changes
    conn.commit()

    #Close the connection
    conn.close()

#Gets all info from testing table
def getTestingData():

    #Connect to database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Gets all data in testing table
    cursor.execute("SELECT * FROM testing")

    testing = cursor.fetchall()

    #Checks the variable has any data in it
    if not testing:
        print("No data found in the table.")
    
    #Close the connection
    conn.close()

    return testing

'''
# Data for generating people - Made by ChatGPT
first_names = ["Alice", "Benjamin", "Charlie", "Diana", "Ethan", "Fatima", "George", "Hannah", "Isaac", "Julia",
               "Kyle", "Leila", "Marcus", "Nora", "Owen", "Priya", "Quentin", "Rania", "Samir", "Tara",
               "Umar", "Victoria", "William", "Xena", "Yusuf", "Zara", "Amara", "Bruno", "Carmen", 
               "Dario", "Elena", "Farah", "Gianni", "Harper",
                "Ibrahim", "Jade", "Kaito", "Lara", "Mateo", "Nina", "Orion", "Pooja", "Quinn",
                "Rafael", "Sofia", "Tariq", "Uma", "Vera", "Waleed", "Xander", "Yara", "Zain",
                "Anya", "Boris", "Chloe", "Dev", "Esme", "Faisal", "Giselle", "Hugo", "Inaya",
                "João", "Keira", "Luca", "Mila", "Noor", "Omar", "Pavel", "Rina", "Sami", "Thalia"]

last_names = ["Johnson", "Lee", "Patel", "Smith", "Zhang", "Rahman", "O'Connor", "Williams", "Kim", "Park",
              "Brown", "Nguyen", "Silva", "Elmi", "Green", "Desai", "Dubois", "Mendez", "Khan", "Blake",
              "Ahmed", "Taylor", "Clark", "Singh", "Turner", "Adams","Abdi", "Bennett", "Chowdhury", "Diaz", "Eriksen", "Fujimoto", "Gonzalez", "Hassan",
            "Iversen", "Jenkins", "Kaur", "Lopez", "Mendoza", "Nakamura", "Okafor", "Paterson",
            "Qureshi", "Rodriguez", "Singh", "Takahashi", "Uddin", "Valdez", "Wong", "Xu",
            "Yilmaz", "Zhou", "Ali", "Baker", "Cissé", "Dubois", "Elias", "Fleming", "Griffin",
            "Hughes", "Ivanov", "Jones", "Kowalski", "Larsen", "Müller", "Nguyen", "O'Shea",
            "Popov", "Rossi", "Silva", "Tanaka", "Uzun", "Vega", "West", "Yamada", "Zhang"]

sports = getSports()

# Function to generate 100 unique people
def generate_people(num_people=100):
    people = set()
    while len(people) < num_people:
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(18, 85)
        skill = random.randint(1, 5)
        sessions = random.randint(2, 14)
        session_length = random.randint(20, 180)
        sport = random.choice(sports)
        people.add((name, age, skill, sessions, session_length, sport))
    return list(people)

people_data = generate_people(100)
'''