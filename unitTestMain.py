import pytest
from unittest.mock import patch
import main

#pytest Code\unitTestMain.py

#Fixtures and Sample Data
@pytest.fixture
def sampleWorkoutPlan():
    return {"Day 1": ["stretch", "stretch", "exercise", "exercise"]}

@pytest.fixture
def samplePopulation():
    return {
        "plan 1": {"Day 1": ["Squat", "Plank"], "Day 2": ["Push-up", "Deadlift"]},
        "plan 2": {"Day 1": ["Crunch", "Sit-up"], "Day 2": ["Lunge", "Jump Rope"]},
    }

@pytest.fixture
def sampleConstraints():
    return {
        "constraintExercise": "",
        "constraintExerciseSens": "",
        "preferredExercise": "",
        "preferredExerciseSens": "",
        "constraintMuscle": "",
        "constraintMuscleSens": "",
        "preferredMuscle": "",
        "preferredMuscleSens": ""
    }

#Core Function Tests
def testSessionSplit():
    stretchNumber, exerciseNumber, plan, totalNumber = main.sessionSplit(3, 60)
    assert stretchNumber == 2
    assert exerciseNumber == 5
    assert totalNumber == 7
    assert len(plan) == 3

def testNegativeSessionSplit():
    stretchNumber, exerciseNumber, plan, totalNum = main.sessionSplit(3, 10)
    assert stretchNumber >= 0
    assert exerciseNumber >= 0

def testStartingPopulation(sampleWorkoutPlan):
    population = main.startingPop(5, sampleWorkoutPlan, 2, 2)
    assert len(population) == 5
    for plan in population.values():
        for day in plan.values():
            assert len(day) == 4  # 2 stretches + 2 exercises

def testFillWorkout(sampleWorkoutPlan):
    filledPlan = main.fillWorkout(sampleWorkoutPlan, 2, 2)
    for day, exercises in filledPlan.items():
        assert len(exercises) == 4
        assert all(isinstance(ex, str) for ex in exercises)

def testSelection(samplePopulation):
    fitness = {"plan 1": 0.5, "plan 2": 0.2}
    selected = main.selection(samplePopulation, fitness, 2)
    assert len(selected) == len(samplePopulation)
    assert any(plan in selected for plan in samplePopulation)

def testCrossover():
    parent1 = {"Day 1": ["Squat", "Plank"], "Day 2": ["Lunge", "Push-up"]}
    parent2 = {"Day 1": ["Deadlift", "Crunch"], "Day 2": ["Jump Rope", "Sit-up"]}
    child = main.crossover(parent1, parent2)
    assert len(child) == len(parent1)
    for day in child:
        assert all(ex in (parent1[day] + parent2[day]) for ex in child[day])

def testMutationChange():
    population = {"plan 1": {"Day 1": ["Squat", "Plank"]}}
    populationCopy = {"plan 1": {"Day 1": ["Squat", "Plank"]}}
    mutated = main.mutation(population.copy(), 1.0)
    assert mutated != populationCopy

def testMutationNoChange():
    population = {"plan 1": {"Day 1": ["Squat", "Plank"]}}
    populationCopy = {"plan 1": {"Day 1": ["Squat", "Plank"]}}
    mutated = main.mutation(population.copy(), 0.0)
    assert mutated == populationCopy

def testRestDays():
    bestPlan = {"Day 1": ["Squat", "Deadlift"], "Day 2": ["Push-up", "Plank"]}
    muscleGroupDay = {"Day 1": "Legs", "Day 2": "Upper Body"}
    updatedPlan = main.restDays(bestPlan, muscleGroupDay)
    assert "Legs Day (Day 1)" in updatedPlan
    assert "Upper body Day (Day 2)" in updatedPlan

#User Input Function Tests
def testEmptyName():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("", 25, 3, 5, 60, "football", "")
    assert result == "Input Error, Name cannot be empty!"

def testEmptyAge():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", "", 3, 5, 60, "football", "")
    assert result == "Input Error, Please enter a valid age (positive integer)."

def testInvalidAgeNegative():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", -1, 3, 5, 60, "football", "")
    assert result == "Age must be a positive number."

def testInvalidAgeTooHigh():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 150, 3, 5, 60, "football", "")
    assert result == "Must be a reasonable human age."

def testInvalidSkill():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 6, 5, 60, "football", "")
    assert result == "Input Error, Please select a valid experience level (1-5)."

def testEmptySkill():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, "", 5, 60, "football", "")
    assert result == "Input Error, Please select a valid experience level (1-5)."

def testInvalidSessionNumberLong():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 3, 20, 60, "football", "")
    assert result == "Sessions per week must be a positive number, and can only have up to 14 per week."

def testInvalidSessionNumberShort():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 3, 0, 60, "football", "")
    assert result == "Sessions per week must be a positive number, and can only have up to 14 per week."

def testEmptySessionNumber():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 3, "", 60, "football", "")
    assert result == "Input Error, Please enter a valid number of sessions per week."

def testInvalidSessionLengthShort():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 3, 5, 0, "football", "")
    assert result == "Session length must be a positive number and above 20 minutes."

def testInvalidSessionLengthLong():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 3, 5, 300, "football", "")
    assert result == "Sessions longer than three hours are not allowed."

def testEmptySessionLength():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 3, 5, "", "football", "")
    assert result == "Input Error, Please enter a valid session length (positive integer)."

def testEmptySport():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 3, 5, 60, "", "")
    assert result == "Input Error, Sport cannot be empty!"

def testValidInputs():
    result, age, skill, sessionNumber, sessionLength, feedback = main.inputValidation("John", 25, 3, 5, 60, "football", "")
    assert result == ""

#Fitness Function Tests
@patch('main.database.getSportSpecific')
@patch('main.database.getExercisesSpecific')
def testFitnessCalc(mock_getExercisesSpecific, mock_getSportSpecific, samplePopulation, sampleConstraints):
    mock_getSportSpecific.return_value = (1, 'soccer', 0.4, 0.6, 'quads, hamstrings, core')
    mock_getExercisesSpecific.return_value = (34, 'bodyweight squats', 1, 'none', 'Anaerobic', 'quads, glutes')

    fitness, _ = main.fitnessCalc('soccer', samplePopulation, 4, 3, sampleConstraints)
    assert all(isinstance(val, float) for val in fitness.values())

#LLM Constraints Test
@patch('main.database.getExercises')
@patch('main.database.getMuscleGroups')
@patch('main.client.chat.completions.create')
def testLlmConstraints(mock_create, mock_getMuscles, mock_getExercises):
    mock_getExercises.return_value = ["Squat", "Deadlift"]
    mock_getMuscles.return_value = ["Legs", "Back"]
    mock_create.return_value.choices = [
        type('', (), {'message': type('', (), {
            'content': '{"constraintExercise": "Squat", "constraintExerciseSens": "5", "preferredExercise": "", "preferredExerciseSens": "", "constraintMuscle": "Legs", "constraintMuscleSens": "5", "preferredMuscle": "", "preferredMuscleSens": ""}'
        })()})]

    feedback = "Avoid squats, my legs hurt"
    constraints = main.llmConstraints(feedback)
    assert constraints["constraintExercise"] == "Squat"
    assert constraints["constraintMuscle"] == "Legs"

#Genetic Algorithm Smoke Test
def testGeneticAlgorithmSmoke():
    workoutPlan = {'Day 1': ['stretch', 'stretch', 'exercise', 'exercise']}
    plan, fitness = main.geneticAlgorithm(workoutPlan, 2, 2, 'football', 4, 3, '')
    assert isinstance(plan, dict)
    assert isinstance(fitness, float)
    assert len(plan) > 0

#Ant Colony Optimization (ACO) Smoke Test
def testAntColonyOptimizationSmoke():
    stretchNumber = 2
    exerciseNumber = 2
    sessionNumber = 2
    totalNumber = 4
    skill = 3
    feedback = ""
    sport = "football"

    plan, fitness = main.antColonyOptimization(
        stretchNumber, exerciseNumber, sport, totalNumber, skill,
        feedback, sessionNumber
    )

    assert isinstance(plan, dict)
    assert isinstance(fitness, float)
    assert len(plan) == sessionNumber

#Simulated Annealing (SA) Smoke Test
def testSimulatedAnnealingSmoke():
    workoutPlan = {
        'Day 1': ['stretch', 'stretch', 'exercise', 'exercise'],
        'Day 2': ['stretch', 'stretch', 'exercise', 'exercise']
    }
    stretchNumber = 2
    exerciseNumber = 2
    totalNumber = 4
    skill = 3
    feedback = ""
    sport = "football"

    plan, fitness = main.simulatedAnnealing(
        stretchNumber, exerciseNumber, sport, totalNumber, skill,
        feedback, workoutPlan
    )

    assert isinstance(plan, dict)
    assert isinstance(fitness, float)
    assert len(plan) == 2
