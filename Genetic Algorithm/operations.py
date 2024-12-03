import random
import numpy as np

def select_population(population, probabilities, population_size):
    selected_indices = np.random.choice(len(population), size=population_size, p=probabilities)
    return [population[i] for i in selected_indices]

def crossover_population(population):
    offspring = []
    for i in range(0, len(population), 2):
        if i+1 < len(population):
            parent1 = population[i]
            parent2 = population[i+1]
            crossover_point = random.randint(0, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            offspring.extend([child1, child2])
        else:
            offspring.append(population[i])
    return offspring

def mutate_population(population, mutation_rate):
    mutated_population = []
    for individual in population:
        new_individual = individual.copy()
        for i in range(len(new_individual)):
            if random.random() < mutation_rate:
                activity, _, _, _ = new_individual[i]
                new_individual[i] = (
                    activity,
                    random.choice(room_capacity.keys()),
                    random.choice(["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]),
                    random.choice(["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"])
                )
        mutated_population.append(new_individual)
    return mutated_population
