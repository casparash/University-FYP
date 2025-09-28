#All prodcued by ChatGPT and edited slightly by me

import time
import matplotlib.pyplot as plt
from main import (
    geneticAlgorithm,
    simulatedAnnealing,
    antColonyOptimization,
    sessionSplit,
    llmConstraints as original_llmConstraints
)

# === Patch the LLM function to avoid OpenAI calls ===
def mock_llmConstraints(feedback):
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

import main
main.llmConstraints = mock_llmConstraints  # Override LLM call

# === Set test parameters ===
session_lengths = list(range(20, 120, 5))
session_number = 3
sport = "football"
skill = 3
feedback = ""
iterations = list(range(5, 100, 5))
size = list(range(5, 100, 5))

# === Containers for results ===
ga_times = []
sa_times = []
aco_times = []

# === Loop through session lengths and profile ===
for iter_count, session_len, size_count in zip(iterations, session_lengths, size):
    stretch_num, exercise_num, workout_plan, total_num = sessionSplit(session_number, session_len)

    # GA
    start = time.perf_counter()
    geneticAlgorithm(workout_plan.copy(), stretch_num, exercise_num,
                     sport, total_num, skill, feedback,
                     iterations=iter_count, size = size_count)
    ga_times.append(time.perf_counter() - start)

    # SA
    start = time.perf_counter()
    simulatedAnnealing(stretch_num, exercise_num, sport, total_num,
                       skill, feedback, workout_plan.copy(),
                       iterations=iter_count)
    sa_times.append(time.perf_counter() - start)

    # ACO
    start = time.perf_counter()
    antColonyOptimization(stretch_num, exercise_num, sport, total_num,
                          skill, feedback, session_number,
                          iterations=iter_count, size = size_count)
    aco_times.append(time.perf_counter() - start)


# === Plot the results ===
plt.figure(figsize=(12, 6))
plt.plot(iterations, ga_times, label='Genetic Algorithm')
plt.plot(iterations, sa_times, label='Simulated Annealing')
plt.plot(iterations, aco_times, label='Ant Colony Optimization')
plt.xlabel("iterations")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time vs. iterations")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Restore original LLM function if needed ===
main.llmConstraints = original_llmConstraints

import numpy as np

# === Extend iterations for projection ===
full_iterations = list(range(5, 200, 5))  # Project beyond measured range (e.g. up to 200)

# === Define time complexity models ===
def time_complexity_ga(n): return n**3 
def time_complexity_sa(n): return n**2
def time_complexity_aco(n): return n**3

# === Normalize predicted times to match measured data scale ===
def normalize(predicted, measured):
    factor = max(measured) / max(predicted[:len(measured)])
    return [p * factor for p in predicted]

# === Generate predicted times ===
ga_pred = normalize([time_complexity_ga(n) for n in full_iterations], ga_times)
sa_pred = normalize([time_complexity_sa(n) for n in full_iterations], sa_times)
aco_pred = normalize([time_complexity_aco(n) for n in full_iterations], aco_times)

# === Plot Everything ===
plt.figure(figsize=(12, 6))

# Measured
plt.plot(iterations, ga_times, 'o-', label='GA Measured')
plt.plot(iterations, sa_times, 's-', label='SA Measured')
plt.plot(iterations, aco_times, '^-', label='ACO Measured')

# Predicted & Projected
plt.plot(full_iterations, ga_pred, 'x--', label='GA Predicted')
plt.plot(full_iterations, sa_pred, 'd--', label='SA Predicted')
plt.plot(full_iterations, aco_pred, '*--', label='ACO Predicted')

plt.xlabel("Iterations")
plt.ylabel("Execution Time (seconds)")
plt.title("Measured vs Predicted Time Complexity with Future Projection")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()