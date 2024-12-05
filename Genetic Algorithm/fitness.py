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
    "SLA101A": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA101B": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA191A": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA191B": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA201": ["Glen", "Banks", "Zeldin", "Shaw"],
    "SLA291": ["Lock", "Banks", "Zeldin", "Singer"],
    "SLA303": ["Glen", "Zeldin", "Banks"],
    "SLA304": ["Glen", "Banks", "Tyler"],
    "SLA394": ["Tyler", "Singer"],
    "SLA449": ["Tyler", "Singer", "Shaw"],
    "SLA451": ["Tyler", "Singer", "Shaw"]
}

other_facilitators = {
    "SLA101A": ["Numen", "Richards"],
    "SLA101B": ["Numen", "Richards"],
    "SLA191A": ["Numen", "Richards"],
    "SLA191B": ["Numen", "Richards"],
    "SLA201": ["Numen", "Richards", "Singer"],
    "SLA291": ["Numen", "Richards", "Shaw", "Tyler"],
    "SLA303": ["Numen", "Singer", "Shaw"],
    "SLA304": ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"],
    "SLA394": ["Richards", "Zeldin"],
    "SLA449": ["Zeldin", "Uther"],
    "SLA451": ["Zeldin", "Uther", "Richards", "Banks"]
}

def fitness(schedule):
    fitness_score = 0
    facilitator_schedule_count = {}
    facilitator_time_slots = {}
    facilitator_activities = {}
    activity_times = {}
    activity_rooms = {}

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

# Track facilitator schedules
        if facilitator not in facilitator_schedule_count:
            facilitator_schedule_count[facilitator] = 0
            facilitator_time_slots[facilitator] = set()
            facilitator_activities[facilitator] = []
        facilitator_schedule_count[facilitator] += 1
        facilitator_time_slots[facilitator].add(time)
        facilitator_activities[facilitator].append((activity, time))

        # Track activity times for specific activities
        if activity not in activity_times:
            activity_times[activity] = []
        activity_times[activity].append(time)

        # Track activity rooms for specific activities
        if activity not in activity_rooms:
            activity_rooms[activity] = []
        activity_rooms[activity].append(room)

    # Facilitator Overscheduling Rules
    for facilitator, count in facilitator_schedule_count.items():
        if facilitator == "Tyler" and count < 2:
            # No penalty for Dr. Tyler if overseeing less than 2 activities
            continue
        elif count < 2:
            fitness_score -= 0.4  # Penalty for overseeing less than 2 activities
        elif count > 5:
            fitness_score -= 0.5  # Penalty for overseeing more than 5 activities

    # Time Slot Overlap Penalties and Rewards
    for facilitator, time_slots in facilitator_time_slots.items():
        for time in time_slots:
            activities_at_time = sum(1 for _, _, t, f in schedule if f == facilitator and t == time)
            if activities_at_time == 1:
                fitness_score += 0.2  # Reward for overseeing 1 activity at a time slot
            elif activities_at_time > 1:
                fitness_score -= 0.2  # Penalty for overseeing more than 1 activity at a time slot

    # Activity-Specific Consecutive Scheduling Check
    for facilitator, activities in facilitator_activities.items():
        activities.sort(key=lambda x: x[1])  # Sort activities by time
        for i in range(1, len(activities)):
            previous_activity, previous_time = activities[i - 1]
            current_activity, current_time = activities[i]
            if current_time == previous_time:  # Consecutive scheduling in the same time slot
                fitness_score -= 0.2  # Penalty for consecutive scheduling in the same time slot

    # Activity Pair Time Distance Rule
    for activity_pair in [("SLA101A", "SLA101B"), ("SLA191A", "SLA191B")]:
        times_a = activity_times.get(activity_pair[0], [])
        times_b = activity_times.get(activity_pair[1], [])
        for time_a in times_a:
            for time_b in times_b:
                time_diff = abs(int(time_a.split()[0]) - int(time_b.split()[0]))
                if time_diff > 4:
                    fitness_score += 0.5  # Reward if activities are more than 4 hours apart
                elif time_a == time_b:
                    fitness_score -= 0.5  # Penalty if activities are scheduled at the same time

    # Reward for SLA191 and SLA101 Intermission Rule
    activity_pairs = [
        ("SLA101A", "SLA191A"), ("SLA101A", "SLA191B"),
        ("SLA101B", "SLA191A"), ("SLA101B", "SLA191B"),
        ("SLA191A", "SLA101A"), ("SLA191A", "SLA101B"),
        ("SLA191B", "SLA101A"), ("SLA191B", "SLA101B")
    ]
    for activity_101, activity_191 in activity_pairs:
        times_101 = activity_times.get(activity_101, [])
        times_191 = activity_times.get(activity_191, [])
        for time_101 in times_101:
            for time_191 in times_191:
                time_diff = abs(int(time_101.split()[0]) - int(time_191.split()[0]))
                if time_diff == 2:  # 2 hours apart means 1 hour intermission between start times, if all activities are 1 hour long
                    fitness_score += 0.25  # Reward for having 1 hour intermission
                elif time_101 == time_191:
                    fitness_score -= 0.25  # Penalty if SLA101 and SLA191 are scheduled at the same time

    # Penalty for Consecutive SLA191 and SLA101 not in Roman or Beach
    for activity_group in [("SLA101A", "SLA101B"), ("SLA191A", "SLA191B")]:
        rooms_a = activity_rooms.get(activity_group[0], [])
        rooms_b = activity_rooms.get(activity_group[1], [])
        for room_a, room_b in zip(rooms_a, rooms_b):
            if room_a in ["Roman 216", "Roman 201", "Beach 201", "Beach 301"] and room_b in ["Roman 216", "Roman 201", "Beach 201", "Beach 301"]:
                continue  # Both are in Roman or Beach
            else:
                fitness_score -= 0.4  # Penalty if not both are in Roman or Beach

    return fitness_score

