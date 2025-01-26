from data import room_cap, expected_enroll, pref_facil, alt_facil, roman_beach, time_cache, ACTIVITIES

def roman_or_beach(previous_room, current_room):
    # A single function to verify if the roman/beach condition is valid
    return (previous_room in roman_beach
            and current_room in roman_beach) or \
           (previous_room not in roman_beach
            and current_room not in roman_beach)


def eval_room(room, activity, room_cap, expected_enroll):
    # Room Size Fitness Evaluation
    adj = 0
    capacity = room_cap[room]
    expected = expected_enroll[activity]
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


def facil_pref(facilitator, activity, pref_facil, alt_facil):
    # Facilitator Preferences
    adj = 0
    if facilitator in pref_facil.get(activity, []):
        adj = 0.5
    elif facilitator in alt_facil.get(activity, []):
        adj = 0.2
    else:
        adj = -0.1
    
    return adj


def time_overlap(fac_sched):
    # Evaluates penalties and rewards for time slot overlaps for each facilitator.
    # dict[str, {Set[str], List[(str, str)]}] -> float

    adj = []
    for fac, sched in fac_sched.items():
        times = sched["times"]  # Set of all time slots assigned to the facilitator
        for time in times:
            # Count the number of activities in this specific time slot
            act_count = sum(1 for _, t in sched["acts"] if t == time)
            if act_count == 1:
                adj.append(0.2)  # Reward for overseeing 1 activity in the time slot
            elif act_count > 1:
                adj.append(-0.2)  # Penalty for overseeing multiple activities simultaneously
    
    return adj


def check_consecutive_time_slots(room_a, room_b,):
    adj = 0
    if not roman_or_beach(room_a, room_b):
            adj = -0.4  # Should help deter large travel distance from Roman or Beach to other rooms
    
    return adj


def check_sla_specific_rules(filtered_activities, filtered_rooms, time_cache):
    # SLA101 and SLA191 Specific Checks
    adj = []

    for i in range(len(filtered_activities)):
        for j in range(i + 1, len(filtered_activities)):         
            same = (("101" in filtered_activities[i] and filtered_activities[j]) or ("191" in filtered_activities[i] and filtered_activities[j]))
            alternating = (("101" in filtered_activities[i] and "191" in filtered_activities[j]) or("101" in filtered_activities[j] and "191" in filtered_activities[i]))

            time_diff = time_delta(filtered_activities[i], filtered_activities[j], time_cache)

            # For being at the same time, regardless of same activity grouping or alternating
            if time_diff == 0:
                if same:
                    adj.append(-0.5)
                elif alternating:
                    adj.append(-0.25)

            # Verifies consecutive & ONLY for SLA101 & SLA191 activity pairs
            elif time_diff == 1 and alternating:
                adj.append(0.5 + check_consecutive_time_slots(filtered_rooms[i], filtered_rooms[j]))
            
            # Verifies hour break & SLA101 & SLA191 activity pair
            elif time_diff == 2 and alternating:
                adj.append(0.25)

            # For being widely spaced apart, in the same activity group only
            elif time_diff > 5 and same:
                adj.append(0.5)

            # Assumes that it is spaced apart, but in SLA101 & SLA191 activity pair or some other unknown case: returns adj = 0

    return round(adj, 2)

def fac_oversched(fac_sched):
    adj = []
    for fac, count in fac_sched.items():
        if count > 4:
            adj.append(0.5)  # Penalty for overseeing more than 5 activities
        elif count <= 2 and fac != "Tyler":
            adj.append(-0.4)
    
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


def room_overlap(current_index, next_index, ACTIVITIES, act_rooms, time_diff):
    adj = []
    
    current_act = ACTIVITIES[current_index]
    current_room = act_rooms[current_act]
    
    for i in range(next_index, 11):
        next_act = ACTIVITIES[next_index]
        next_room = act_rooms[next_act]
        if time_diff == 0 and current_room == next_room:
            adj.append(-0.5)

    return adj


def time_delta(time_a, time_b, time_cache):
    time_diff = abs(time_cache[time_a] - time_cache[time_b])
    return time_diff


def fitness(schedule):
    # Stage 1: Schedule Pre-processing
    fac_sched = {}
    act_rooms = {activity: None for activity in ACTIVITIES}
    act_times = {activity: None for activity in ACTIVITIES}

    for index, act in enumerate(ACTIVITIES):
        fac = schedule[act]["facilitator"]
        time = act_times[act] = schedule[act]["time"]
        room = act_rooms[act] = schedule[act]["room"]

        # Helper data types specific for this schedule only
        fac_sched = track_fac_sched(time, act, fac, fac_sched)
    
    filtered_activities = [act for act in schedule if "101" in act or "191" in act]
    filtered_rooms = [schedule[act]["room"] for act in schedule if "101" in act or "191" in act]

    #Stage 2: Schedule Processing via Fitness Evaluation
    fitness_score = 0
    scores = []
    i = 1
    
    for index, act in enumerate(ACTIVITIES):
        
        room_score = eval_room(act_rooms[ACTIVITIES[index]], act, room_cap, expected_enroll)
        scores.append(room_score)
        
        facil_score = facil_pref(schedule[act]["facilitator"], act, pref_facil, alt_facil)
        scores.append(facil_score)
        
        if i < 11:
            time_diff = time_delta(act_times[ACTIVITIES[index]], act_times[ACTIVITIES[i]], time_cache)
            overlap_score = room_overlap(index, i, ACTIVITIES, act_rooms, time_diff)
            scores.extend(overlap_score)
            i += 1
    
    sched_score = fac_oversched(fac_sched)
    scores.extend(sched_score)    

    time_score = time_overlap(fac_sched)
    scores.extend(time_score)

    specific_score = check_sla_specific_rules(filtered_activities, filtered_rooms, time_cache)
    scores.extend(specific_score)

    fitness_score = sum(scores)
    return round(fitness_score, 2)
