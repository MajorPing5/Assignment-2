from data import room_cap, expected_enroll, pref_facil, alt_facil, roman_beach, time_cache, ACTIVITIES

def roman_or_beach(previous_room, current_room):
    # A single function to verify if the roman/beach condition is valid
    return (previous_room in roman_beach
            and current_room in roman_beach) or \
           (previous_room not in roman_beach
            and current_room not in roman_beach)


def eval_room(room, act, room_cap, expected_enroll):
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
            act_count = sum(1 for t in sched["acts"] if t == time)
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


def specific_rules(filtered_activities, filtered_rooms, filtered_times, time_cache):
    # SLA101 and SLA191 Specific Checks
    adj = []
    debug_info = []

    for i in range(len(filtered_activities)):
        for j in range(i + 1, len(filtered_activities)):         
            same = (((filtered_activities[i].startswith("SLA101")) and (filtered_activities[j].startswith("SLA101"))) or
                    ((filtered_activities[i].startswith("SLA191")) and (filtered_activities[j].startswith("SLA191"))))
            
            alternating = ((filtered_activities[i].startswith("SLA101") and filtered_activities[j].startswith("SLA191")) or
                           (filtered_activities[j].startswith("SLA101") and filtered_activities[i].startswith("SLA191")))

            time_diff = time_delta(filtered_times[i], filtered_times[j], time_cache)

            # Add debug information for this comparison
            debug_info.append({
                "pair": (filtered_activities[i], filtered_activities[j]),
                "same": same,
                "alt": alternating,
                "time_diff": time_diff,
            })

            match time_diff:
                case 0:
                    if same:
                        adj.append(-0.5)
                    elif alternating:
                        adj.append(-0.25)
                
                case 1:
                    if alternating:
                        adj.append(
                            round(0.5 + check_consecutive_time_slots(filtered_rooms[i],
                                                                     filtered_rooms[j]),
                            2))
                
                case 2:
                    if alternating:
                        adj.append(0.25)
                
                case _:
                    if time_diff > 5 and same:
                        adj.append(0.5)
                    else:
                        adj.append(0)

    return adj, debug_info


def check_facilitator_consecutive(facilitator, fac_sched, act_rooms, act_times):
    adj = []  # Store penalties or rewards

    # Sort the facilitator's times using time_cache for numerical order
    times = sorted(list(fac_sched[facilitator]["times"]), key=lambda t: time_cache[t])

    # Iterate through consecutive time slot pairs
    for i in range(len(times) - 1):
        current_time = times[i]
        next_time = times[i + 1]

        # Check if the time slots are consecutive
        if time_delta(current_time, next_time, time_cache) == 1:
            # Find the activities corresponding to the consecutive times
            current_act = next(act for act in fac_sched[facilitator]["acts"] if act_times[act] == current_time)
            next_act = next(act for act in fac_sched[facilitator]["acts"] if act_times[act] == next_time)

            # Retrieve the rooms for these activities
            current_room = act_rooms[current_act]
            next_room = act_rooms[next_act]

            # Call the consecutive room check function and append its result
            adj.append(check_consecutive_time_slots(current_room, next_room))

    return adj


def fac_oversched(fac_sched):
    adj = []
    for fac, details in fac_sched.items():
        count = details["count"]
        if count > 4:
            adj.append(-0.5)  # Penalty for overseeing more than 4 activities
        elif count <= 2 and fac != "Tyler":
            adj.append(-0.4)
        else:
            adj.append(0)
    
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
    act_rooms = {activity: "" for activity in ACTIVITIES}
    act_times = {activity: "" for activity in ACTIVITIES}

    for index, act in enumerate(ACTIVITIES):
        fac = schedule[act]['facilitator']
        time = act_times[act] = schedule[act]['time']
        room = act_rooms[act] = schedule[act]['room']

        # Helper data types specific for this schedule only
        fac_sched = track_fac_sched(time, act, fac, fac_sched)
    
    filtered_activities = [act for act in schedule if "101" in act or "191" in act]
    filtered_rooms = [schedule[act]['room'] for act in schedule if "101" in act or "191" in act]
    filtered_times = [schedule[act]['time'] for act in schedule if "101" in act or "191" in act]

    #Stage 2: Schedule Processing via Fitness Evaluation
    fitness_score = 0
    scores = []
    i = 1
    
    for index, act in enumerate(ACTIVITIES):
        
        room_score = eval_room(act_rooms[ACTIVITIES[index]], act, room_cap, expected_enroll)
        scores.append(room_score)
        
        facil_score = facil_pref(schedule[act]['facilitator'], act, pref_facil, alt_facil)
        scores.append(facil_score)
        


        if i < 11:
            time_diff = time_delta(act_times[ACTIVITIES[index]], act_times[ACTIVITIES[i]], time_cache)
            overlap_score = room_overlap(index, i, ACTIVITIES, act_rooms, time_diff)
            scores.extend(overlap_score)
            i += 1
    
    for facilitator, sched in fac_sched.items():
        # Only process facilitators with more than 1 activity assigned
        if sched["count"] > 1:
            consecutive_adj = check_facilitator_consecutive(facilitator, fac_sched, act_rooms, act_times)
            scores.extend(consecutive_adj)

    sched_score = fac_oversched(fac_sched)
    scores.extend(sched_score)    

    time_score = time_overlap(fac_sched)
    scores.extend(time_score)

    specific_score = specific_rules(filtered_activities, filtered_rooms, filtered_times, time_cache)
    scores.extend(specific_score)

    fitness_score = sum(scores)
    return round(fitness_score, 2)
