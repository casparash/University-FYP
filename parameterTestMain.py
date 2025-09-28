import main
import cProfile
import pstats
import random

'''
def randomSearchSA(trials):
    bestFitnessOverTrials = []
    
    bestParams = None
    bestScore = float('inf')

    for _ in range(trials):
        print("Running...")
        #Randomly sample hyperparameters
        initialTemp = random.randint(1000, 5000)
        coolingRate = random.uniform(0.85, 0.99)
        iterations = random.randint(500, 3000)
        mutationRate = random.uniform(0.1, 0.3)

        #Run simulated annealing with sampled parameters
        plan, score = main.simulatedAnnealing(
            stretchNumber = 3,  
            exerciseNumber = 6,
            sport = "american football",
            totalNumber = 9,
            skill = 3,
            feedback = "",
            workoutPlan = {'Day 1': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise'], 
                            'Day 2': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise'], 
                            'Day 3': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise']},
            initialTemp = initialTemp, 
            coolingRate = coolingRate, 
            iterations = iterations, 
            mutationRate = mutationRate
        )

        #Track best configuration
        if score < bestScore:
            bestScore = score
            bestParams = (initialTemp, coolingRate, iterations, mutationRate)

        bestFitnessOverTrials.append(bestScore)

    print(f"Best Parameters: {bestParams} with Score: {bestScore}")

    return bestFitnessOverTrials

bestFitnessOverTrials = randomSearchSA(50)

def randomSearchGA(trials):
    bestFitnessOverTrials = []

    bestParams = None
    bestScore = float('inf')

    for _ in range(trials):
        print("Running...")
        #Randomly sample hyperparameters
        size = random.randint(50, 200)
        mutationRate = random.uniform(0.01, 0.3)
        generations = random.randint(100, 500)
        
        plan, score = main.geneticAlgorithm(
            workoutPlan = {'Day 1': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise'], 
                            'Day 2': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise'], 
                            'Day 3': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise']}, 
            stretchNumber = 3, 
            exerciseNumber = 6, 
            sport = "american football", 
            totalNumber = 9,
            skill = 3, 
            feedback = "",
            size = size,
            mutationRate = mutationRate,
            generations = generations)
        

        #Track best configuration
        if score < bestScore:
            bestScore = score
            bestParams = (size, mutationRate, generations)

        bestFitnessOverTrials.append(bestScore)

    print(f"Best Parameters: {bestParams} with Score: {bestScore}")

    return bestFitnessOverTrials

bestFitnessOverTrials = randomSearchGA(50)

def randomSearchACO(trials):
    bestFitnessOverTrials = []

    bestParams = None
    bestScore = float('inf')

    for _ in range(trials):
        print("Running...")
        #Randomly sample hyperparameters
        numAnts = random.randint(20, 100)
        iterations = random.randint(10, 100)
        evaporationRate = random.uniform(0.05, 0.3)
        
        plan, score = main.antColonyOptimization(
            stretchNumber = 3, 
            exerciseNumber = 6, 
            sport = "american football", 
            totalNumber = 9,
            skill = 3, 
            feedback = "",
            sessionNumber = 3,
            numAnts = numAnts,
            iterations = iterations,
            evaporationRate = evaporationRate)
        

        #Track best configuration
        if score < bestScore:
            bestScore = score
            bestParams = (numAnts, iterations, evaporationRate)

        bestFitnessOverTrials.append(bestScore)

    print(f"Best Parameters: {bestParams} with Score: {bestScore}")

    return bestFitnessOverTrials

bestFitnessOverTrials = randomSearchACO(100)
'''

def profileGA():

    main.geneticAlgorithm(
        workoutPlan = {'Day 1': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise'], 
                        'Day 2': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise'], 
                        'Day 3': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise']}, 
        stretchNumber = 3, 
        exerciseNumber = 6, 
        sport = "american football", 
        totalNumber = 9,
        skill = 3, 
        feedback = "I’ve injured my leg and I want to do more press ups")

cProfile.run('profileGA()', 'profileResults')

p = pstats.Stats('profileResults')
p.strip_dirs().sort_stats('cumulative').print_stats(10)

def profileSA():

    main.simulatedAnnealing(
            stretchNumber = 3,  
            exerciseNumber = 6,
            sport = "american football",
            totalNumber = 9,
            skill = 3,
            feedback = "I’ve injured my leg and I want to do more press ups",
            workoutPlan = {'Day 1': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise'], 
                            'Day 2': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise'], 
                            'Day 3': ['stretch', 'stretch', 'stretch', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise']})

cProfile.run('profileSA()', 'profileResults')

p = pstats.Stats('profileResults')
p.strip_dirs().sort_stats('cumulative').print_stats(10)

def profileACO():

    main.antColonyOptimization(
            stretchNumber = 3, 
            exerciseNumber = 6, 
            sport = "american football", 
            totalNumber = 9,
            skill = 3, 
            feedback = "I’ve injured my leg and I want to do more press ups",
            sessionNumber = 3)

cProfile.run('profileACO()', 'profileResults')

p = pstats.Stats('profileResults')
p.strip_dirs().sort_stats('cumulative').print_stats(10)


