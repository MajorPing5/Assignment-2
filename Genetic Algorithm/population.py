import random
from data import ACTIVITIES, ROOMS, TIMES, FACILITATORS


def generate_random_population(population_size):
    # Generates the initial population of schedules.
    # Args: \
    #    population_size (int): The number of schedules to generate.
    # Returns:\
    #    list: A list of randomly generated schedules.

    def generate_random_schedule():
        # Generates a single random schedule with activity-centric keys.
        # Returns:
        #     schedule = {activity: {"time": str, "room": str, "facilitator": str}}
        
        schedule = {}
        for activity in ACTIVITIES:
            room = random.choice(ROOMS)
            facilitator = random.choice(FACILITATORS)
            time = random.choice(TIMES)
            schedule[activity] = {
                "time": time,
                "room": room,
                "facilitator": facilitator
            }
        return schedule


    # Generate a list of random schedules
    return [generate_random_schedule() for _ in range(population_size)]
