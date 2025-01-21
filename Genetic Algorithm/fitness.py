from data import room_cap, expected_enroll, pref_facil, alt_facil, roman_beach, time_cache, activity_pairs

def roman_or_beach(previous_room, current_room):
    # A single function to verify if the roman/beach condition is valid
    return (previous_room in roman_beach
            and current_room in roman_beach) or \
           (previous_room not in roman_beach
            and current_room not in roman_beach)


def eval_room(room, activity, room_capacity, expected_enrollment):
    # Room Size Fitness Evaluation
    adj = 0
    capacity = room_capacity[room]
    expected = expected_enrollment[activity]
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


def facil_pref(facilitator, activity, preferred_faciltator, alternative_facilitator):
    # Facilitator Preferences
    adj = 0 # Adjustment identifier to be used on fitness score outside of function
    if facilitator in preferred_faciltator.get(activity, []):
        adj = 0.5
    elif facilitator in alternative_facilitator.get(activity, []):
        adj = 0.2
    else:
        adj = -0.1
    
    return adj


def time_overlap(fac_sched):
    # Evaluates penalties and rewards for time slot overlaps for each facilitator.
    # dict[str, {Set[str], List[(str, str)]}] -> float

    adj = 0
    for fac, sched in fac_sched.items():
        times = sched["times"]  # Set of all time slots assigned to the facilitator
        for time in times:
            # Count the number of activities in this specific time slot
            act_count = sum(1 for _, t in sched["acts"] if t == time)
            if act_count == 1:
                adj = 0.2  # Reward for overseeing 1 activity in the time slot
            elif act_count > 1:
                adj = -0.2  # Penalty for overseeing multiple activities simultaneously
    
    return adj


def check_consecutive_time_slots(time_diff, room_a, room_b,):

    # Determines feasibility and a practical, efficient schedule for facilitators.    
    if time_diff == 1:  # Consecutive time slots (e.g., 10 AM & 11 AM)
        adj = 0.5
        if not roman_or_beach(room_a, room_b):
            adj -= 0.4  # Should help deter large travel distance from Roman or Beach to other rooms
    elif time_diff == 2:  # 2 hours apart means 1 hour intermission
        adj = 0.25
    elif time_diff == 0:
        adj = -0.25  # Should help deter being at the same time
    
    return round(adj, 2)


def check_sla_specific_rules(time_diff, activity_pair):
    # SLA101 and SLA191 Specific Checks
    adj = 0
    for activity_pair in [("SLA101A", "SLA101B"), ("SLA191A", "SLA191B")]:
        if time_diff > 4:
            adj = 0.5  # Reward if activities are more than 4 hours apart
        elif time_a == time_b:
            adj = -0.5  # Penalty if activities are scheduled at the same time
    
    return adj

 
# Helps track facilitators activity load to prevent overload of assignment
def track_fac_sched(time, act, fac, fac_sched):
    new_sched = fac_sched.copy()


    if fac not in new_sched:
        new_sched[fac] = {"count": 0, "times": set(), "acts": []}
    new_sched[fac]["count"] += 1
    new_sched[fac]["times"] = new_sched[fac]["times"].union({time})
    new_sched[fac]["acts"] = new_sched[fac]["acts"] + [act]

    return new_sched


def time_delta(time_a, time_b, time_cache):
    time_diff = abs(time_cache[time_a] - time_cache[time_b])
    return time_diff


def fitness(schedule):
    # Stage 1: Schedule Pre-processing
    fac_sched = {}
    act_rooms = {}
    act_times = {}

    for act, details in schedule.items():
        time = details["time"]
        room = details["room"]
        fac = details["facilitator"]

        # Helper data types specific for this schedule only
        fac_sched = track_fac_sched(time, act, fac, fac_sched)
        act_rooms[act] = room
        act_times[act] = time
    
    sla_time_data = {
        act: schedule[act]["time"]
        for act in ["SLA101A", "SLA101B", "SLA191A", "SLA191B"]
        if act in schedule
    }

    #Stage 2: Schedule Processing via Fitness Evaluation
    fitness_score = 0

    for time, act, room, fac in schedule:
        
        fitness_score = eval_room(room, act, room_cap, expected_enroll)
        fitness_score = facil_pref(fac, act, pref_facil, alt_facil)
    
    # Facilitator Overscheduling Rules
    for fac, count in fac_sched.items():
        if count > 4:
            fitness_score -= 0.5  # Penalty for overseeing more than 5 activities
        elif count <= 2 and fac != "Tyler":
            fitness_score -= 0.4

    fitness_score += time_overlap(fac_sched)

    # Activity-Specific Consecutive Scheduling Check
    for fac, act in facilitator_activities.items():
        act.sort(key=lambda x: x[1])  # Sort activities by time
        for i in range(1, len(act)):
            previous_activity, previous_time = act[i - 1]
            current_activity, current_time = act[i]
            
            if current_time == previous_time:  # Consecutive scheduling in the same time slot
                fitness_score -= 0.2  # Penalty for consecutive scheduling in the same time slot

    # Reward for SLA191 and SLA101 Intermission Rule
    for activity_101, activity_191 in activity_pairs:
        times_101 = act_times.get(activity_101, [])
        times_191 = act_times.get(activity_191, [])
        for time_101 in times_101:
            for time_191 in times_191:
                time_diff = abs(int(time_101.split()[0]) - int(time_191.split()[0]))
                if time_diff == 2:  # 2 hours apart means 1 hour intermission between start times, if all activities are 1 hour long
                    fitness_score += 0.25  # Reward for having 1 hour intermission
                elif time_101 == time_191:
                    fitness_score -= 0.25  # Penalty if SLA101 and SLA191 are scheduled at the same time

    # Penalty for Consecutive SLA191 and SLA101 not in Roman or Beach
    for act_a, act_b in [("SLA101A", "SLA101B"), ("SLA191A", "SLA191B")]:
        time_diff = time_delta(schedule["SLA101A"], schedule["SLA101B"], time_cache)
        adj = check_sla_specific_rules(sla_time_data, time_diff)
        fitness_score += adj

    return fitness_score
