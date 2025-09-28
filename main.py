import sqlite3
import random
from collections import Counter
from openai import OpenAI
import numpy as np
import json
import threading
import time
import database
import html

#The API key
client = OpenAI(
  api_key=""
)

#Calls the ChatGPT API with the feedback provided by the user
def llmConstraints(feedback):

    #Creating constraints dict, this is used if there is no feedback
    constraints = {
    "constraintExercise": "",
    "constraintExerciseSens": "",
    "preferredExercise": "",
    "preferredExerciseSens": "",
    "constraintMuscle": "",
    "constraintMuscleSens": "",
    "preferredMuscle": "",
    "preferredMuscleSens": ""
    }

    #Gets all the exercises in the db
    exerciseList = database.getExercises()

    #Gets all the muscle groups in the db
    muscleGroups = database.getMuscleGroups()

    #If there is feedback
    if len(feedback) != 0:

        #The prompt that will be sent to ChatGPT
        prompt = f"""
        You are an expert workout assistant. Carefully analyze the user's feedback to extract workout constraints with accurate mappings and sensitivity scoring.

        ### Task:
        1. **Injury Detection**:
        - If the user mentions pain, injury, or discomfort (e.g., "hurt", "injured", "pain") in a specific area, map it to the corresponding **muscle group(s)** and assign a sensitivity score of **5** (highest priority to avoid).
        - Example: "I hurt my leg" → **Quads, Hamstrings, Calves** with sensitivity **5**.

        2. **Mapping Terms to Muscle Groups**:
        - General terms like:
            - "leg" → **Quads, Hamstrings, Calves**
            - "back" → **Lats, Traps, Lower Back**
            - "arm" → **Biceps, Triceps, Forearms**

        3. **Sensitivity Scoring**:
        - **5**: Explicit issues or strong language (e.g., injuries, "must avoid", "never").
        - **3**: Moderate preference/avoidance ("prefer", "avoid if possible").
        - **1**: Weak mentions or general references.

        5. **Strict Matching**:
        - Only use exercises and muscle groups from the provided lists.
        - **Do not** infer or suggest exercises not mentioned or implied.
        - **Avoid duplicates** in the output.

        ### Feedback:
        {feedback}

        ### List of Allowed Exercises:
        {exerciseList}

        ### List of Allowed Muscle Groups:
        {muscleGroups}

        ### Output Format (Valid JSON):
        {{
            "constraintExercise": "<Matched exercise(s) to avoid>",
            "constraintExerciseSens": "<sensitivity>",
            "preferredExercise": "<Matched exercise(s) to prioritize>",
            "preferredExerciseSens": "<sensitivity>",
            "constraintMuscle": "<Matched muscle group(s) to avoid>",
            "constraintMuscleSens": "<sensitivity>",
            "preferredMuscle": "<Matched muscle group(s) to focus on>",
            "preferredMuscleSens": "<sensitivity>"
        }}

        - Only return valid JSON. If a constraint is not mentioned, use an empty string.
        - Do not include Markdown formatting (like triple backticks).
        """
        #The API call
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        #Saves the response from the API and parses it so can be used later
        responseText = completion.choices[0].message.content
        #print(responseText)
        constraints = json.loads(responseText)

    #print(constraints)

    return constraints

#Calls another ChatGPT API with the workout plan, sport, and user skill in order to rate it
def llmAsAJudge(bestPlan, sport, skill):

    #prompt that will be sent to the LLM
    prompt = f"""
    You are an expert in sports and exercise workouts. Analyze the sport-specific gym workout plan provided and evaluate it based on the following catagories.

    ### Task: 
    1. **Difficulty Scoring**
    - Score how well the difficulty of the workout plan matches the users skill on a scale of 1 to 5 where 1 is terrible and 5 is amazing. 
    - Skill level = 1 then the user is not experianced at all, and skill level = 5 then they are very experianced.
    - It should be based on the skill level of the user and should be a balanced so not too easy or too difficult.

    2. **Sport Focus Scoring**
    - Score how applicable to the sport they are training the workout plan is on a scale of 1 to 5 (The same as task 1).
    - The workout plan should be balanced by being a good general workout plan but focusing on exercises/muscles that will help with the chosen sport.

    3. **Overall Rating**
    - Score the workout on a scale of 1 to 5 (The same as task 1).
    - Keep in mind the sport and the difficulty score.

    4. **Additional Comments**
    - Add at least one sentance explaining your score for both difficulty and sport focus.
    - Add any changes you would advise if there are any.
    - Add a short sentance with any general comments about the workout.

    ### Workout Plan:
    {bestPlan}

    ### Sport:
    {sport}

    ### Skill Level:
    {skill}

    ### Output Format (Valid JSON):
        {{
            "Difficulty": "<How well the workout plan matched the users skill, scale of 1 - 5>",
            "Sport Focus": "<How well the workout plan matched the sport, scale of 1 - 5>",
            "Overall Rating": "<The overall rating of the workout plan, scale of 1 - 5>",
            "Additional Comments": "<All addtional comments>"
        }}

    Only return valid JSON. If a constraint is not mentioned, use an empty string.
    """
    #The API call
    completion = client.chat.completions.create(
        model="o3-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    #Saves the response from the API and parses it so can be used later
    responseText = completion.choices[0].message.content
    llmEvaluation = json.loads(responseText)

    #print(llmEvaluation)

    return llmEvaluation

#This function checks through the user inputs from the GUI to make sure they are reasonable
def inputValidation(name, age, skill, sessionNumber, sessionLength, sport, feedback):
    
    #Create and fill error variable, in case of no errors
    error = ""
    
    #Make sure name isnt empty
    if not name:
        error = "Input Error, Name cannot be empty!"

    #Try to make age into an int
    try:
        age = int(age)

        #Make sure age is positive and possible for human
        if age <= 0:
            error = "Age must be a positive number."
        elif age > 100:
            error = "Must be a reasonable human age."
        
    except ValueError:
        error = "Input Error, Please enter a valid age (positive integer)."

    #Try to make skill and int
    try:
        skill = int(skill)

        #Make sure skill is within range of 1-5
        if skill <= 0:
            error = "Input Error, Please select a valid experience level (1-5)."
        elif skill > 5:
            error = "Input Error, Please select a valid experience level (1-5)."

    except ValueError:
        error = "Input Error, Please select a valid experience level (1-5)."

    #Try to make session number and int
    try:
        sessionNumber = int(sessionNumber)

        #make sure its a reasonable number of sessions per week
        if sessionNumber <= 1:
            error = "Sessions per week must be a positive number, and can only have up to 14 per week."
        elif sessionNumber > 14:
            error = "Sessions per week must be a positive number, and can only have up to 14 per week."
        
    except ValueError:
        error = "Input Error, Please enter a valid number of sessions per week."

    #Try to make session number and int
    try:
        sessionLength = int(sessionLength)

        #Make sure its a positive number and less than three hours
        if sessionLength < 20:
            error = "Session length must be a positive number and above 20 minutes."
        elif sessionLength > 180:
            error = "Sessions longer than three hours are not allowed."
        
    except ValueError:
        error = "Input Error, Please enter a valid session length (positive integer)."

    #Make sure sport is not empty
    if not sport:
        error = "Input Error, Sport cannot be empty!"

    #Limits feedback to 100 characters, as to not cost me too much in LLM costs
    if len(feedback) > 100:
        error = "Your feedback is too long, please shorten it to under 100 characters"

    #Replace any special character
    feedback = html.escape(feedback)

    #Replace other special characters
    for char in ['{', '}', '#']:
        feedback = feedback.replace(char, '')

    return error, age, skill, sessionNumber, sessionLength, feedback

#Deciding on the split between stretches and exercises each day, as well as how many can fit into the day
def sessionSplit(sessionNumber, sessionLength):

    #Splitting time into stretches and normal exercises as they take different amount of time per exercise
    stretchTime = (20 / 100) * sessionLength
    exerciseTime = (80 / 100) * sessionLength

    #Translating the time into amount of exercises that will fit in each session
    stretchNumber = round(stretchTime / 5)
    exerciseNumber = round(exerciseTime / 10)

    #Setting the variable to the correct amount of exercises
    totalNumber = stretchNumber + exerciseNumber

    #Create the dictionary
    workoutPlan = {f"Day {i+1}": [] for i in range(sessionNumber)}

    #Fill the days workout with placeholder
    for day in workoutPlan:
        workoutPlan[day] = ["stretch"] * stretchNumber + ["exercise"] * exerciseNumber
    
    #print(stretchNumber, exerciseNumber, workoutPlan)
    
    return stretchNumber, exerciseNumber, workoutPlan, totalNumber

#Calculating the fitness of the workout (Lower is better)
def fitnessCalc(sport, population, totalNumber, skill, constraints):

    #Connect to the database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Fetch the row from database that matches the sport chosen by the user
    cursor.execute("SELECT * FROM sports WHERE sport LIKE ?", ('%' + sport + '%',))
    resultFitness = cursor.fetchone()

    #Check if there are any results
    if not resultFitness:
        conn.close()

        print("There is no sport with that name")

        return None, None

    #Save results to varibales
    id, sport, anaerobic, aerobic, muscles = resultFitness

    #Depending on the difference the fitness will be more or less harshly effected
    difference = (anaerobic - aerobic) * 1
    amountType = 1 - (difference / 10)
    
    #Decide the main sport type
    if anaerobic > aerobic:
        sportType = "anaerobic"
    elif aerobic > anaerobic:
        sportType = "aerobic"
    else:
        sportType = ""
    
    #Makes muscles into list so they can be compared
    muscles = muscles.strip().lower().split(", ")

    #Create fitness dict
    fitness = {}

    #Create a list to store muscle groups
    previousMuscleGroups = []
    
    #Goes through each exercise in each day in each workout plan
    for plan, workoutPlan in population.items():

        #sets the fitness as 1 at the start
        fitness[plan] = 1.0

        #Create daily fitness and exercise lists
        dailyFitness = []
        allExercises = []

        #Create a dict to store the muscle groups for the day
        muscleGroupDay = {}

        #Goes through each day in the current workout plan
        for day, exercises in workoutPlan.items():

            #Set the daily fitness as 1
            fitness[day] = 1.0

            #Create list that saves the muscle groups of each exercise
            allMuscleGroups = []

            #Adds each exercise to list
            allExercises.extend(exercises)

            #Goes through each exercise
            for exercise in exercises:

                #Takes type from the database where the exercise matches
                cursor.execute("SELECT type FROM exercises WHERE exercise = ?", (exercise,))
                resultType = cursor.fetchone()
                
                #Checks to make sure we are looking at an exercise and not a stretch
                if resultType and resultType[0].strip().lower() != "stretch":

                    #If the type (anaerobic/aerobic) is the same then it lowers fitness for the day
                    if resultType and resultType[0].strip().lower() == sportType:

                        #Lowers fitness based on the amount the types are different (More difference means more exercises in the higher type)
                        fitness[day] *= amountType
    
                #Get muscle groups from database where the exercises matches
                cursor.execute("SELECT muscleGroups FROM exercises WHERE exercise = ?", (exercise,))
                resultMuscleGroups = cursor.fetchone()
                
                #Checks there are results
                if resultMuscleGroups:

                    #Seperates the muscle groups
                    resultMuscleGroups = resultMuscleGroups[0].strip().lower().split(", ")
                else:
    
                    resultMuscleGroups = [] 
                
                #If there are items in the constaintsExercise column
                if constraints['constraintExercise']:
                    
                    #Takes the data and saves under variables
                    exerciseData = constraints['constraintExercise'].lower().split(', ')
                    sensitivity = int(constraints['constraintExerciseSens'])
                    
                    #Reduces the fitness based on if any exercises match and scaling on sensitivity
                    if exercise in exerciseData:
                        fitness[day] *= (sensitivity/10 + 1) 
                        
                #If there are items in the preferredExercise column
                if constraints['preferredExercise']:
                    
                    #Takes the data and saves under variables
                    exerciseData = constraints['preferredExercise'].lower().split(', ')
                    sensitivity = int(constraints['preferredExerciseSens'])
                    
                    #Increases the fitness based on if any exercises match and scaling on sensitivity
                    if exercise in exerciseData:
                        fitness[day] *= (sensitivity/10) 

                #If there are items in the constraintMuscle column
                if constraints['constraintMuscle']:
                    
                    #Takes the data and saves under variables
                    muscleData = constraints['constraintMuscle'].lower().split(', ')
                    sensitivity = int(constraints['constraintMuscleSens'])
                    
                    #Reduces the fitness based on if any exercises match and scaling on sensitivity
                    if any(muscle in muscleData for muscle in resultMuscleGroups):
                        fitness[day] *= (sensitivity/10 + 1) 

                #If there are items in the preferredMuscle column  
                if constraints['preferredMuscle']:
                    
                    #Takes the data and saves under variables
                    muscleData = constraints['preferredMuscle'].lower().split(', ')
                    sensitivity = int(constraints['preferredMuscleSens'])
                    
                    #Increases the fitness based on if any exercises match and scaling on sensitivity
                    if any(muscle in muscleData for muscle in resultMuscleGroups):
                        fitness[day] *= (sensitivity/10) 
                        
                #Adds to list of all muscle groups in the day
                allMuscleGroups.extend(resultMuscleGroups)

                #Compares to see if they match muscle groups of sport
                matchingMuscles = [muscle for muscle in muscles if muscle in resultMuscleGroups]

                #The more matching muscle groups there are the more it lowers the fitness
                if len(matchingMuscles) == 3:
                    fitness[day] *= 0.8
                elif len(matchingMuscles) == 2:
                    fitness[day] *= 0.9
                elif len(matchingMuscles) == 1:
                    fitness[day] *= 0.95

                #Gets the difficulty from the database where the exercises matches
                cursor.execute("SELECT difficulty FROM exercises WHERE exercise = ?", (exercise,))
                resultDifficulty = cursor.fetchone()

                #Checks if anything was returned
                if resultDifficulty:
                    resultDifficulty = resultDifficulty[0]
                else:
                    resultDifficulty = 0

                #If the difficulty of the exercise is smaller than or equal to the skill then it lowers the fitness 10%
                if resultDifficulty <= skill:
                    fitness[day] *= 0.9

            #Looks for how many times each muscle group show up per day
            allMuscleGroupsCount = Counter(allMuscleGroups)

            if allMuscleGroupsCount:

                #Saves the muscles group with the highest count
                highestMuscleGroup = max(allMuscleGroupsCount, key=allMuscleGroupsCount.get)

                muscleGroupDay[day] = highestMuscleGroup

                #Saves the count of the highest count muscle group
                highestCount = allMuscleGroupsCount[highestMuscleGroup]

                #Lowers fitness for the day if the count is higher
                fitness[day] *= (1 - (highestCount / 10))
            else:
                muscleGroupDay[day] = "General"

            #If the length of the plan is larger than 1 day
            if len(population['plan 1']) >= 1:

                #Checks for how many muscle groups of the current and previous day match
                overlap = sum(1 for muscles in allMuscleGroups if muscles in previousMuscleGroups)

                #If there are any it decreases fitness based on how many
                if overlap == 0:
                    fitness[day] *= 0.7
                elif 2 > overlap > 0:
                    fitness[day] *= 0.9

            #Updates muscle group list for the next day
            previousMuscleGroups = allMuscleGroups

            #Adds daily fitness to the list of fitnesses
            dailyFitness.append(fitness[day])

        #Counts the number of each exercises
        exerciseCount = Counter(allExercises)

        #Goes through the count of each exercise and saves the amount of duplicates there are
        duplicates = sum(count - 1 for count in exerciseCount.values() if count > 1)

        #If there are any duplicates then the fitness is raised by an amount calculated on the number of duplicates (More duplicates = higher fitness)
        if duplicates > 0:
            penalty = (duplicates / totalNumber) / 10 
            dailyFitness = [value + penalty for value in dailyFitness]
        
        #Works out the fitness for the whole plan by finding the avarage of each day
        averageFitness = sum(dailyFitness) / len(dailyFitness)
        fitness[plan] = averageFitness

    #Close connection to database
    conn.close()

    return fitness, muscleGroupDay

#Fills the initial workout plan from the database
def fillWorkout(workoutPlan, stretchNumber, exerciseNumber):

    #Connect to the database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Fetch all stretches and exercises and save to lists
    cursor.execute("SELECT exercise FROM exercises WHERE type = 'Stretch'")
    stretches = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT exercise FROM exercises WHERE type != 'Stretch'")
    exercises = [row[0] for row in cursor.fetchall()]

    #Close the connection
    conn.close()

    #Goes through each day in the plan
    for day in workoutPlan:

        #Randomly select stretches and exercises
        selected_stretches = random.sample(stretches, stretchNumber)
        selected_exercises = random.sample(exercises, exerciseNumber)

        #Fill the day's workout
        workoutPlan[day] = selected_stretches + selected_exercises

    return workoutPlan

#Creates starting population of workout plans
def startingPop(size, workoutPlan, stretchNumber, exerciseNumber):

    #Make population dict with plans as the keys
    population = {f"plan {i+1}": [] for i in range(size)}

    #Goes through each workout plan
    for plan in population:

        #Creates workout plan dict
        individualWorkoutPlan = {day: [] for day in workoutPlan}

        #Calls the fillWorkout function to fill it
        individual = fillWorkout(individualWorkoutPlan, stretchNumber, exerciseNumber)

        #Adds it to the population
        population[plan] = individual
    
    return population

#Use tournament selection to pick best plan
def selection(population, fitness, tournamentSize):

    #Create selected dict
    selected = {}

    #Goes through each workout plan in population
    for i in range(len(population)):
        
        #Takes a random sample of plans
        tournament = random.sample(list(population.keys()), tournamentSize)
        
        #Compares fitness, plan with the lowest is saved as winner
        winner = min(tournament, key=lambda plan: fitness[plan])

        #Adds winner to population with new key
        selected[f"plan {i+1}"] = population[winner]  

    return selected

#Uses uniform crossover on two plans (Parents) to create two new plans (Children)       
def crossover(parent1, parent2):

    #Create new workout plan dict
    child = {}

    #Goes through each day in the parents plan
    for day in parent1.keys():
        
        #For the day create a list
        child[day] = []
        
        #Goes through each exercise of the day
        for i in range(len(parent1[day])):

            #Random 50% on which parent the child takes exercises from for that day
            if random.random() < 0.5:
                child[day].append(parent1[day][i])
            else:
                child[day].append(parent2[day][i])

    return child

#Has a chance of changing a random stretch or exercise in the workout each day
def mutation(nextPopulation, mutationRate):

    #Connect to the database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Fetch all exercises and save to list
    cursor.execute("SELECT exercise FROM exercises WHERE type != 'Stretch'")
    allExercises = [row[0] for row in cursor.fetchall()]

    #Fetch all stretches and save to list
    cursor.execute("SELECT exercise FROM exercises WHERE type = 'Stretch'")
    allStretches = [row[0] for row in cursor.fetchall()]

    #Close the connection
    conn.close()

    #Goes through each plan
    for plan, days in nextPopulation.items():

            #Goes through each day
            for day, exercises in days.items():

                #For every exercise
                for i in range(len(exercises)):  

                    #Checks if random number is smaller that mutation rate
                    if random.random() < mutationRate:  
                        
                        #Find a new strecth/exercise to replace it
                        if exercises[i] in allStretches and allStretches:
                            nextPopulation[plan][day][i] = random.choice(allStretches)
                       
                        elif allExercises:
                            nextPopulation[plan][day][i] = random.choice(allExercises)
    
    return nextPopulation

#Changes the name of each day to reflect muscle group being worked on
def restDays(bestPlan, muscleGroupDay):
    
    #Create new dict
    updatedPlan = {}

    #Goes through each day in the plan
    for day, value in bestPlan.items():

        #Finds the most used muscle group for the day
        muscleGroupName = muscleGroupDay.get(day, "General").capitalize()
        
        #Creates day name
        key = f"{muscleGroupName} Day ({day})"

        #Adds to new plan
        if key not in updatedPlan:
            updatedPlan[key] = []

        #Adds exercises to the new plan
        updatedPlan[key].extend(value)
        
    bestPlan = updatedPlan

    return bestPlan

#Gets a random person from the database to use instead of needing imputs (Mainly used for quick testing)
def randomPerson():

    #Connect to the database
    conn = sqlite3.connect("exercises_sports.db")
    cursor = conn.cursor()

    #Gets one random person the the people table in the database and saves to variable
    cursor.execute("SELECT * FROM people ORDER BY RANDOM() LIMIT 1")
    resultPerson = cursor.fetchone()

    #Close the connection
    conn.close()

    #Saves individual varibales from the columns
    name, age, skill, sessionNumber, sessionLength, sport = resultPerson

    #Makes sport all lower case
    sport = sport.lower()

    #print(resultPerson)

    return name, age, skill, sessionNumber, sessionLength, sport

#Main function that uses many of the previous functions to run a genetic algorithm to create a workout plan
def geneticAlgorithm(workoutPlan, stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback):

    #Setting variables used to run algorithm, saved here for easy access and editing
    size = 161
    mutationRate = 0.05
    generations = 270
    
    #Calls the feedback function for the constraints
    constraints = llmConstraints(feedback)

    #Created a starting population of workout plans
    population = startingPop(size, workoutPlan, stretchNumber, exerciseNumber)
    
    #Goes through each generation
    for generation in range(generations):

        #Finds the fitness of the workout plans
        fitness, muscleGroupDay = fitnessCalc(sport, population, totalNumber, skill, constraints)

        #Saves the plan with the lowest fitness
        bestPlan = min(population, key=fitness.get)
        bestFitness = fitness[bestPlan]

        #Uses tournament selection to find the best plans and saves them in new population
        selectedPopulation = selection(population, fitness, tournamentSize=3)

        #Creates dict for the next generation
        nextPopulation = {}

        #Goes through each plan 2 at a time
        for i in range(0, len(selectedPopulation), 2):

            #Pick 2 plans (Parents)
            parentNames = random.sample(list(selectedPopulation.keys()), 2)
            parent1 = selectedPopulation[parentNames[0]]
            parent2 = selectedPopulation[parentNames[1]]

            #Generate 2 children using crossover of the 2 parents
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent1, parent2)

            #Add children to next population
            nextPopulation[f"plan {i+1}"] = child1
            nextPopulation[f"plan {i+2}"] = child2

        #Puts the next population through mutation
        nextPopulation = mutation(nextPopulation, mutationRate)

        #Saves the next population over the old population for next generation
        population = nextPopulation

        #print(fitness[bestPlan])

    #Saves plan with best fitness
    bestPlan = population[bestPlan]

    #Calls restDays to add day names
    bestPlan = restDays(bestPlan, muscleGroupDay)

    return bestPlan, bestFitness

#gets the heurisitc value for ACO (Higher is better)
def heuristic(exercise, muscles, sportType, skill, difference):
    
    #Setting variables, higher number means they are more important
    weightDifficulty = 0.2
    weightMuscle = 0.4
    weightType = 0.4
    
    #gets the exercise specified from the db
    result = database.getExercisesSpecific(exercise)

    #Saves the resluts to variables
    id, exercise, difficulty, equipment, type, muscleGroups = result

    #Saves muscle groups used
    muscleGroups = muscleGroups.strip().lower().split(", ")
    
    #If exercise is more difficult then the users skill set to 0
    difficultyScore = 0 if difficulty > skill else 1

    #Calculates how many of the muscle groups match
    matchedMuscles = set(muscleGroups).intersection(set(muscles))
    muscleMatchScore = len(matchedMuscles) / len(muscleGroups)

    #If the exercise if the same type then it increases the score by the difference
    typeMatchScore = (difference + 1) if type == sportType or type == "" else 0

    #Calculates the heurisitc using the score and weight
    heuristic = (weightDifficulty * difficultyScore +
                weightMuscle * muscleMatchScore +
                weightType * typeMatchScore)
        
    return heuristic

#Selects an exercise based on pheromones and heuristics
def selectExercise(pheromones, heuristics, visited):
    
    #Setting variables that will change how the pheromones/heurisitc is weighted
    alpha = 1
    beta = 2

    #Create a new list
    probabilities = []

    #Goes through each exercises
    for i in range(len(pheromones)):

        #Checks if the exercise has been visited
        if i not in visited:

            #Created probability based on varibles from start and saves to list
            prob = (pheromones[i] ** alpha) * (heuristics[i] ** beta)
            probabilities.append(prob)
        else:
           
            #If exercise has been visited then its updated to 0
            probabilities.append(0)

    #Saves the total probability
    total = sum(probabilities)

    #Saves the probability of each exercise based on previous calculations
    probabilities = [p / total if total > 0 else 0 for p in probabilities]

    #Picks random exercises based on the probability
    workout = np.random.choice(range(len(pheromones)), p=probabilities) 
    
    return workout

#Updates the pheromones for the exercises
def updatePheromones(pheromones, allPlans, allScores, evaporationRate):
    
    #Setting the rate at which pheromones are set
    depositFactor = 1.0
    
    #updates pheromones with the evaporation rate
    pheromones = [p * (1 - evaporationRate) for p in pheromones]

    #Saves the best score
    maxScore = max(allScores)

    #Goes through each plan
    for plan, score in zip(allPlans, allScores):

        #Goes through each day
        for dayName, dayExercise in plan.items():

            #Goes through each exercise
            for exercise in dayExercise:
                
                #If the exercise has a pheromone
                if exercise in pheromones:

                    #Update it based on how good the score is comaprd to the max score
                    pheromones[exercise] += depositFactor * (score / maxScore)

    return pheromones

#Main function for running ant colony optimization
def antColonyOptimization(stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback, sessionNumber):

    #Setting variables that dictate how it runs  
    numAnts = 37
    iterations = 78
    evaporationRate = 0.29

    #Gets any constraints after calling the API with feedback
    constraints = llmConstraints(feedback)

    #Gets all exercises of the two types and saves
    allAnaerobic = database.getExercisesType("Anaerobic")
    allAerobic = database.getExercisesType("Aerobic")

    #Saves all exercises (except stretches) together
    allExercises = allAnaerobic + allAerobic

    #Gets all stretches from db
    allStretches = database.getExercisesType("Stretch")

    #Sets pheromones for each exercise and strech
    pheromonesExercise = [1.0 for _ in allExercises]
    pheromonesStretch = [1.0 for _ in allStretches]
    
    #Gets info about the sport chosen from db
    result = database.getSportSpecific(sport)

    #Saves results of db call to variables
    id, sport, anaerobic, aerobic, muscles = result
    muscles = muscles.strip().lower().split(", ")

    #Finds the difference between the sport types
    difference = (anaerobic - aerobic) * 1
    
    #Sets sport type (Same as in fitness function)
    if anaerobic > aerobic:
        sportType = "anaerobic"
    elif aerobic > anaerobic:
        sportType = "aerobic"
    else:
        sportType = ""

    #Sets heuristics for each exercise 
    heuristics = [heuristic(exercise, muscles, sportType, skill, difference) for exercise in allExercises]
    
    #Sets initial best plan and best fitness variables
    bestPlan = None
    bestFitness = float("inf")

    #For every iteration
    for _ in range(iterations):

        #Resets the plans/fitness' each iteration
        allPlans = []
        allFitness = []

        #For every ant
        for _ in range(numAnts):
            
            #Resets the plan
            plan = {}

            #For every day
            for i in range(sessionNumber):

                #Resets the day plan and set of visited exercises
                dayPlan = []
                visited = set()

                #For every stretch
                for _ in range(stretchNumber):

                    #Select stretches and add to plan
                    idx = selectExercise(pheromonesStretch, heuristics, visited)
                    stretch = allStretches[idx]
                    
                    dayPlan.append(stretch)
                    visited.add(stretch)
                
                #For every exercise
                for _ in range(exerciseNumber):

                    #Select exercises and add to plan
                    idx = selectExercise(pheromonesExercise, heuristics, visited)
                    exercise = allExercises[idx]
                    
                    dayPlan.append(exercise)
                    visited.add(exercise)

                plan[f"Day {i + 1}"] = dayPlan
            
            #"Fill" a population with the plan. so it can be used in the fitness function
            population = {
                "plan 1": plan
            }

            #Find fitness of the plan
            fitness, muscleGroupDay = fitnessCalc(sport, population, totalNumber, skill, constraints)

            #Add to list of all plans
            allPlans.append(plan)

            #Save fitness
            fitness = fitness["plan 1"]
            allFitness.append(fitness)
            
            #If fitness is lower then save as best plan/fitness
            if fitness < bestFitness:
                bestFitness = fitness
                bestPlan = plan

        #Update all pheromones for stretches and exercises
        pheromonesStretch = updatePheromones(pheromonesStretch, allPlans, allFitness, evaporationRate)
        pheromonesExercise = updatePheromones(pheromonesExercise, allPlans, allFitness, evaporationRate)

    #Set names for each day of best plan
    bestPlan = restDays(bestPlan, muscleGroupDay)
    
    return bestPlan, bestFitness

#Main function for running simulated annealing
def simulatedAnnealing(stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback, workoutPlan):

    #Set inital variables
    size = 1
    initialTemp = 4748
    coolingRate = 0.9
    iterations = 621
    mutationRate = 0.28

    #Get constraints from the user feedback
    constraints = llmConstraints(feedback)

    #Create a ranodm starting population
    currentPopulation = startingPop(size, workoutPlan, stretchNumber, exerciseNumber)

    #Find the fitness of the first population
    fitness, muscleGroupDay = fitnessCalc(sport, currentPopulation, totalNumber, skill, constraints)

    #Save the fitness
    currentScore = fitness['plan 1']

    #Save the starting plan as best plan and fitness
    bestPopulation = currentPopulation
    bestScore = currentScore

    #For every iteration
    for _ in range(iterations):

        #Create neighbour population by using mutation
        neighbourPopulation = mutation(currentPopulation, mutationRate)

        #Find fitness of neighbour
        neighbourFitness, muscleGroupDay = fitnessCalc(sport, neighbourPopulation, totalNumber, skill, constraints)

        #Save fitness
        neighbourScore = neighbourFitness['plan 1']

        #Calculate delta through fitness of both plans
        delta = neighbourScore - currentScore

        #If the new plan is better or the random number is lower than the exponential function (The worse the new fitness the less likely)
        if delta > 0 or random.random() < np.exp(delta / initialTemp):
            
            #Save the new plan/fitness over the current plan/fitness
            currentPopulation = neighbourPopulation
            currentScore = neighbourScore

            #If the fitness is lower then save as best plan/fitness
            if currentScore < bestScore:
                bestPopulation = currentPopulation
                bestScore = currentScore
        
        #Lower the temperature by cooling rate
        initialTemp *= coolingRate
    
    #Save the best plan
    bestPlan = bestPopulation['plan 1']

    #Give names to each day
    bestPlan = restDays(bestPlan, muscleGroupDay)
    
    return bestPlan, bestScore

#Function used to test algorithms one at a time, used throughout development process
def testingQuick():
    name, age, skill, sessionNumber, sessionLength, sport = randomPerson()

    feedback = ""

    stretchNumber, exerciseNumber, workoutPlan, totalNumber = sessionSplit(sessionNumber, sessionLength)

    startTime = time.perf_counter()

    bestPlan1 = geneticAlgorithm(workoutPlan, stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback)

    bestPlan2 = antColonyOptimization(stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback, sessionNumber)

    bestPlan3 = simulatedAnnealing(stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback, workoutPlan)

    endTime = time.perf_counter()

    executionTime = endTime - startTime

    #print(bestPlan1)

    #llmEvaluation = llmAsAJudge(bestPlan3, sport, skill)

    print("GA: ", bestPlan1)
    print("ACO: ", bestPlan2)
    print("SA: ", bestPlan3)
    print(executionTime)

#Testing fucntion used to test all algorithms properly
def testing():

    #Gets a random person from people table
    name, age, skill, sessionNumber, sessionLength, sport = randomPerson()

    #Joins variables to create user (For the testing table in db)
    user = ", ".join(map(str, [name, age, skill, sessionNumber, sessionLength, sport]))

    #Set feedback
    feedback = ""

    #Create session split
    stretchNumber, exerciseNumber, workoutPlan, totalNumber = sessionSplit(sessionNumber, sessionLength)

    #Create results dictionary
    results = {}

    #Create wrapper function to save results
    def run_algorithm(name, func, *args):

        #Start time
        start = time.perf_counter()

        #Saves results from algorithms
        bestPlan, bestFitness = func(*args)

        #End time
        end = time.perf_counter()

        #Save results
        results[name] = {
            "bestPlan": bestPlan,
            "bestFitness": bestFitness,
            "time": end - start
        }

    #Create threads for each algorithm
    thread1 = threading.Thread(target=run_algorithm, args=("GA", geneticAlgorithm, workoutPlan, stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback))
    thread2 = threading.Thread(target=run_algorithm, args=("ACO", antColonyOptimization, stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback, sessionNumber))
    thread3 = threading.Thread(target=run_algorithm, args=("SA", simulatedAnnealing, stretchNumber, exerciseNumber, sport, totalNumber, skill, feedback, workoutPlan))

    #Start threads
    thread1.start()
    thread2.start()
    thread3.start()

    #Wait for threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

    '''
    endTime = time.perf_counter()
    executionTime = endTime - startTime

    for algo in results:
        print(f"\n{algo} Results:")
        print("Best Plan:", results[algo]["bestPlan"])
        print("Best Fitness:", results[algo]["bestFitness"])
        print("Execution Time:", results[algo]["time"], "seconds")
    '''

    #For each algorithm
    for algo in results:

        #Get results from LLM
        llmResults = llmAsAJudge(results[algo]["bestPlan"], sport, skill)

        #Create single varibale for plan (Like user at the start)
        plan = ", ".join(f"{key}: {value}" for key, value in results[algo]["bestPlan"].items())

        #Add data to testing table
        database.insertTestingData(algo, results[algo]["time"], results[algo]["bestFitness"], llmResults["Difficulty"], 
                                   llmResults["Sport Focus"], llmResults["Overall Rating"], llmResults["Additional Comments"], plan, user)

#testingQuick()

random.seed(1)
'''
for i in range(100):
    try:
        testing()
        print(f"Test {i+1}/100 complete")
    except Exception as e:
        print(f"Test {i+1} failed: {e}")
'''