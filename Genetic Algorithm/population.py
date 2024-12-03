import random

def generate_random_population(population_size):
    activities = ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA291", "SLA303", "SLA304", "SLA394", "SLA449", "SLA451"]
    rooms = ["Slater 003", "Roman 216", "Loft 206", "Roman 201", "Loft 310", "Beach 201", "Beach 301", "Logos 325", "Frank 119"]
    times = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]
    facilitators = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]
    
    def generate_random_schedule():
        schedule = []
        for activity in activities:
            room = random.choice(rooms)
            time = random.choice(times)
            facilitator = random.choice(facilitators)
            schedule.append((activity, room, time, facilitator))
        return schedule

    return [generate_random_schedule() for _ in range(population_size)]
