import random

# Constants defining the possible values for schedules
ACTIVITIES = ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA291", "SLA303", "SLA304", "SLA394", "SLA449", "SLA451"]
ROOMS = ["Slater 003", "Roman 216", "Loft 206", "Roman 201", "Loft 310", "Beach 201", "Beach 301", "Logos 325", "Frank 119"]
TIMES = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]
FACILITATORS = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]

def generate_random_population(population_size):
    # Generates the initial population of schedules.\
    # \
    # Args: \
    #    population_size (int): The number of schedules to generate.\
    # \
    # Returns:\
    #    list: A list of randomly generated schedules.

    def generate_random_schedule():
        # \
        # Generates a single random schedule where each activity is uniquely assigned \
        # a room, time, and facilitator. \
        # \
        # Returns: \
        #     dict: A schedule organized by time slots, with activities as keys.
        #
        schedule = {time: {} for time in TIMES}  # Initialize with times as keys

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
