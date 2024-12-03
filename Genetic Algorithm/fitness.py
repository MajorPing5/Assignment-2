room_capacity = {
    "Slater 003": 45,
    "Roman 216": 30,
    "Loft 206": 75,
    "Roman 201": 50,
    "Loft 310": 108,
    "Beach 201": 60,
    "Beach 301": 75,
    "Logos 325": 450,
    "Frank 119": 60
}

expected_enrollment = {
    "SLA100A": 50,
    "SLA100B": 50,
    "SLA191A": 50,
    "SLA191B": 50,
    "SLA201": 50,
    "SLA291": 50,
    "SLA303": 60,
    "SLA304": 25,
    "SLA394": 20,
    "SLA449": 60,
    "SLA451": 100
}

preferred_facilitators = {
    "SLA100A": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA100B": ["Glen", "Lock", "Banks", "Zeldin"],
    # Add others here...
}

other_facilitators = {
    "SLA100A": ["Numen", "Richards"],
    "SLA100B": ["Numen", "Richards"],
    # Add others here...
}

def fitness(schedule):
    fitness_score = 0
    for activity, room, time, facilitator in schedule:
        # Room Size Fitness Evaluation
        if room_capacity[room] < expected_enrollment[activity]:
            fitness_score -= 0.5  # Room too small
        elif room_capacity[room] > 3 * expected_enrollment[activity]:
            fitness_score -= 0.2  # Room excessively large
        else:
            fitness_score += 0.3  # Room appropriate

        # Facilitator Preferences
        if facilitator in preferred_facilitators.get(activity, []):
            fitness_score += 0.5
        elif facilitator in other_facilitators.get(activity, []):
            fitness_score += 0.2
        else:
            fitness_score -= 0.1

        # Add more rules here based on the assignment

    return fitness_score
