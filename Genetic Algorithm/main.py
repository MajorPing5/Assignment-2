from ast import Pow
from population import generate_random_population
from fitness import fitness
from operations import select_population, mutate_population
from operations import crossover_population
import numpy as np
from scipy.special import softmax

# Using imports from multiple files helps modularize the code, making it easier to test, maintain, and extend each component separately.
# Consider ensuring that each imported module is placed in the same directory or installed as a package to avoid 'ModuleNotFoundError'.
# When using softmax as an imported function, make sure 'softmax.py' is correctly referenced. It should be either in the same directory or installed properly as a Python module.
# Make sure that the population.py module is in the same directory as main.py or appropriately referenced. Otherwise, Python will not be able to resolve this import.

# Constants
POPULATION_SIZE = 500
GENERATIONS = 100
MUTATION_RATE = 0.01

# Initial Population
population = generate_random_population(POPULATION_SIZE)

# Evolutionary Loop
for generation in range(GENERATIONS):
    # Calculate Fitness Scores
    fitness_scores = [fitness(individual) for individual in population]

    # Softmax Normalization
    probabilities = softmax(fitness_scores)

    # Selection
    selected_population = select_population(population, probabilities, POPULATION_SIZE)

    # Crossover
    offspring_population = crossover_population(selected_population)

    # Mutation
    population = mutate_population(offspring_population, MUTATION_RATE/(Pow(2, generation)))

    # Optional: Print progress at every 10 generations
    if generation % 10 == 0:
        best_index = np.argmax(fitness_scores)
        best_fitness = fitness_scores[best_index]
        print(f"Generation {generation}: Best Fitness = {best_fitness:.2f}")

# Final Evaluation
final_fitness_scores = [fitness(individual) for individual in population]
best_index = np.argmax(final_fitness_scores)
best_schedule = population[best_index]
best_fitness_score = final_fitness_scores[best_index]

# Write Best Schedule to File
output_filename = 'best_schedule_output.txt'
with open(output_filename, 'w') as file:
    # Write the fitness score
    file.write(f"Fitness Score: {best_fitness_score:.2f}\n")
    
    # Write the column headers
    file.write(f"Activity, Room, Facilitator, Time\n")
    
    # Write each activity schedule in order
    for activity, room, time, facilitator in best_schedule:
        file.write(f"{activity}, {room}, {facilitator}, {time}\n")

print(f"Best schedule with fitness score {best_fitness_score:.2f} has been saved to {output_filename}.")
