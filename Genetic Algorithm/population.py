import random
from data import ACTIVITIES, ROOMS, TIMES, FACILITATORS


def generate_random_population(population_size):
    # Generates the initial population of schedules.
    # Args: \
    #    population_size (int): The number of schedules to generate.
    # Returns:\
    #    list: A list of randomly generated schedules.

    def generate_random_schedule():
        # Generates a single random schedule where each activity
        # is uniquely assigned a room, time, and facilitator.
        # Returns: \
        #     schedule = {time: {activity: {room,facilitator}}}

        schedule = {time: {} for time in TIMES}  # Initialize w/ times as keys

        for activity in ACTIVITIES:
            # Randomly select room, facilitator, and time
            room = random.choice(ROOMS)
            facilitator = random.choice(FACILITATORS)
            time = random.choice(TIMES)

            # Assign the activity under the selected time slot
            schedule[time][activity] = {
                "room": room,
                "facilitator": facilitator
            }

        return schedule

    # Generate a list of random schedules
    return [generate_random_schedule() for _ in range(population_size)]
