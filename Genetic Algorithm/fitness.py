from data import room_cap, expected_enroll, pref_facil, alt_facil, roman_or_beach, time_cache

def are_both_in_roman_or_beach(previous_room, current_room):
    """
    Check if both consecutive activities are in either Roman or Beach rooms to
    minimize overall facilitator travel time.
    Helps facilitators have minimal movement between consecutive sessions,
    improving overall schedule feasibility.
    """
    return (previous_room in roman_or_beach
            and current_room in roman_or_beach) or \
           (previous_room not in roman_or_beach
            and current_room not in roman_or_beach)


def eval_room(room, act):
    # Room Size Fitness Evaluation
    adj = 0
    capacity = room_cap[room]
    expected = expected_enroll[act]
    ratio = capacity / expected

    if ratio < 1:
        adj = -0.5  # Room too small
    elif ratio > 6:
        adj = -0.4  # Room excessively large
    elif ratio > 3:
        adj = -0.2  # Room moderately large
    else:
        adj = 0.3  # Room size appropriate
    
    return adj



def room_cap_check(capacity, expected, fitness_score):
    # Room Size Fitness Evaluation
    if capacity < expected:
        fitness_score -= 0.5    # Room too small
    elif capacity > 3 * expected:
        fitness_score -= 0.2    # Room 3x excessively large
    elif capacity > 6 * expected:
        fitness_score -= 0.4    # Room 6x excessively large
    else:
        fitness_score += 0.3  # Room size is appropriate

    return fitness_score


def facil_pref_check(facilitator, act, fitness_score):
    # Facilitator Preferences
    if facilitator in pref_facil.get(act, []):
        fitness_score += 0.5
    elif facilitator in alt_facil.get(act, []):
        fitness_score += 0.2
    else:
        fitness_score -= 0.1
    
    return fitness_score


def check_consecutive_time_slots(time_a, time_b, room_a, room_b, fitness_score):

    # Evaluate the scheduling of consecutive time slots and room locations to determine feasibility and a practical, efficient schedule for facilitators.

    time_a_military = time_cache[time_a]
    time_b_military = time_cache[time_b]
    time_diff = abs(time_b_military - time_a_military)
    if time_diff == 1:  # Consecutive time slots (e.g., 10 AM & 11 AM)
        fitness_score += 0.5
        if not are_both_in_roman_or_beach(room_a, room_b):
            fitness_score -= 0.4  # Should help deter large travel distance from Roman or Beach to other rooms
    elif time_diff == 2:  # 2 hours apart means 1 hour intermission
        fitness_score += 0.25
    elif time_a == time_b:
        fitness_score -= 0.25  # Should help deter being at the same time
    return fitness_score


def check_sla_specific_rules(activity_times, activity_rooms, fitness_score):
    # SLA101 and SLA191 Specific Checks
    for activity_pair in [("SLA101A", "SLA101B"), ("SLA191A", "SLA191B")]:
        times_a = activity_times.get(activity_pair[0], [])
        times_b = activity_times.get(activity_pair[1], [])
        for time_a in times_a:
            for time_b in times_b:
                time_a_military = time_cache[time_a]
                time_b_military = time_cache[time_b]
                time_diff = abs(time_b_military - time_a_military)
                if time_diff > 4:
                    fitness_score += 0.5  # Reward if activities are more than 4 hours apart
                elif time_a == time_b:
                    fitness_score -= 0.5  # Penalty if activities are scheduled at the same timeW


# Helps track facilitators activity load to prevent overload of assignment
def track_fac_sched(fac, act, time, fac_sched):
    if fac not in fac_sched:
        fac_sched[fac] = {"count": 0, "times": set(), "acts": []}
    fac_sched[fac]["count"] += 1
    fac_sched[fac]["times"].add(time)
    fac_sched[fac]["acts"].append((act, time))


def fitness(schedule):
    score = 0
    fac_sched = {}
    act_times = {}
    act_rooms = {}

    for act, room, time, fac in schedule:
        capacity = room_cap[room]
        expected = expected_enroll[act]
        
        fitness_score = eval_room(room, act)

        fitness_score = facil_pref_check(fac, act, fitness_score)        

    # Tracking facilitator schedules, activity times, and rooms to assess schedule quality in subsequent calculations.
        # Activity times for specific activities
        if act not in activity_times:
            activity_times[act] = []
        activity_times[act].append(time)

        # Activity rooms for specific activities
        if act not in activity_rooms:
            activity_rooms[act] = []
        activity_rooms[act].append(room)

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
            if not are_both_in_roman_or_beach(room_a, room_b):
                    fitness_score -= 0.4  # Penalty if not both are in Roman or Beach rooms

    return fitness_score


__all__ = [
    "room_cap_check",
    "facil_pref_check",
    "check_consecutive_time_slots",
    "check_sla_specific_rules",
    "fitness",
]