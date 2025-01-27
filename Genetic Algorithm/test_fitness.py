# test_fitness.py
import unittest
import fitness
import data
from population import generate_random_population


class TestManualSchedule(unittest.TestCase):
    def display_schedule(self, schedule):
        # Display a single schedule in a hierarchical format.
        # Step 1: Transform the data into the desired structure
        transformed_schedule = {}
        for activity, details in schedule.items():
            time = details["time"]
            if time not in transformed_schedule:
                transformed_schedule[time] = {}  # Initialize the time slot
            transformed_schedule[time][activity] = {
                "room": details["room"],
                "facilitator": details["facilitator"]
            }

        # Step 2: Display the hierarchical schedule
        print("Generated Schedule:")
        for time, activities in transformed_schedule.items():
            print(f"Time: {time}")
            if activities:  # If there are activities under this time slot
                for activity, details in activities.items():
                    print(f"  Activity: {activity}")
                    print(f"    Room: {details['room']}")
                    print(f"    Facilitator: {details['facilitator']}")

    @unittest.skip("Skipping manual schedule display to proceed with fitness tests only.")
    def test_generate_and_display_schedule(self):
        # Generate and display one random schedule.
        schedule = generate_random_population(1)[0]  # Extracts schedule

        # Display the schedule
        self.display_schedule(schedule)

        # Pause for manual review
        input("\nPress Enter to close...")

class TestRomanOrBeach(unittest.TestCase):
    def test_roman_or_beach_true(self):
        true_cases = [
            ("Roman 216", "Roman 201"),     # Both Roman
            ("Roman 201", "Roman 216"),     # Both Roman, alt variation
            ("Beach 201", "Beach 301"),     # Both Beach
            ("Beach 301", "Beach 201"),     # Both Beach, alt variation
            ("Loft 206", "Frank 119"),      # Neither Roman nor Beach
        ]
        for previous_room, current_room in true_cases:
            with self.subTest(state="Should Return True", previous_room=previous_room, current_room=current_room):
                self.assertTrue(
                    fitness.roman_or_beach(previous_room, current_room))


    def test_roman_or_beach_false(self):
        false_cases = [
            ("Roman 201", "Loft 206"),  # Only previous room is Roman
            ("Beach 201", "Loft 206"),  # Only previous room is Beach
            ("Loft 206", "Roman 201"),  # Only current room is Roman
            ("Loft 206", "Beach 301"),  # Only current room is Beach
        ]
        for previous_room, current_room in false_cases:
            with self.subTest(state="Should Return False", previous_room=previous_room, current_room=current_room):
                self.assertFalse(
                    fitness.roman_or_beach(previous_room, current_room))
        

class TestConsecutiveTimeSlots(unittest.TestCase):
    def test_SLA_consecutive_valid_time(self):
        # Test valid consecutive time slots.
        test_cases = [
            (1, "Roman 216", "Beach 301", 0.5),  # Both Roman/Beach
            (1, "Loft 206", "Frank 119", 0.5),   # Neither Roman/Beach
        ]
        for time_diff, room_a, room_b, expected in test_cases:
            with self.subTest(time_diff = time_diff, room_a = room_a, room_b = room_b):
                self.assertEqual(
                    fitness.check_consecutive_time_slots(time_diff, room_a, room_b),
                    expected)

    def test_SLA_consecutive_invalid_time(self):
        # Test invalid consecutive time slots.
        invalid_cases = [
            (1, "Roman 216", "Loft 206", 0.1),  # Roman/Other
            (1, "Beach 301", "Loft 206", 0.1),  # Beach/Other
            (1, "Loft 206", "Roman 216", 0.1),  # Other/Roman
            (1, "Loft 206", "Beach 301", 0.1),  # Other/Beach
        ]
        for time_diff, room_a, room_b, expected in invalid_cases:
            with self.subTest(time_diff=time_diff, room_a=room_a, room_b=room_b):
                self.assertEqual(
                    fitness.check_consecutive_time_slots(time_diff, room_a, room_b),
                    expected)

    def test_SLA_one_hour_DeltaT(self):
        # Test cases where time difference is two hours.
        cases = [
            (2, "Roman 201", "Beach 201", 0.25),  # Two hours apart
        ]
        for time_diff, room_a, room_b, expected in cases:
            with self.subTest(time_diff=time_diff, room_a=room_a, room_b=room_b):
                self.assertEqual(
                    fitness.check_consecutive_time_slots(time_diff, room_a, room_b),
                    expected)

    def test_same_time_slots(self):
        # Test cases where the time difference is zero (same time slots).
        cases = [
            (0, "Roman 216", "Beach 301", -0.25),  # Same time slots
        ]
        for time_diff, room_a, room_b, expected in cases:
            with self.subTest(time_diff=time_diff, room_a=room_a, room_b=room_b):
                self.assertEqual(
                    fitness.check_consecutive_time_slots(time_diff, room_a, room_b),
                    expected)


class TestRoomEvaluation(unittest.TestCase):
    def test_eval_room(self):
        test_cases = [
            ("Room A", "Activity 1", {"Room A": 50}, {"Activity 1": 60}, -0.5),     # Room too small
            ("Room B", "Activity 2", {"Room B": 50}, {"Activity 2": 51}, -0.5),     # Room cap = expected - 1 -> Barely considered too small
            ("Room C", "Activity 3", {"Room C": 50}, {"Activity 3": 50}, 0.3),      # Room cap = expected -> Perfect size
            ("Room D", "Activity 4", {"Room D": 150}, {"Activity 4": 50}, 0.3),     # Room cap = 3*expected -> At max acceptable size
            ("Room E", "Activity 5", {"Room E": 151}, {"Activity 5": 50}, -0.2),    # Room cap > 3*expected -> First discrete value over acceptable size
            ("Room F", "Activity 6", {"Room F": 300}, {"Activity 6": 50}, -0.2),    # Room cap = 6*expected -> At max allowed tier 1 too big
            ("Room G", "Activity 7", {"Room G": 301}, {"Activity 7": 50}, -0.4)     # Room cap > 6*expected - > First discrete value of excessive large room
        ]

        for room, activity, room_capacity, expected_enrollment, expected in test_cases:
            with self.subTest(room=room, activity=activity):
                actual = fitness.eval_room(room, activity, room_capacity, expected_enrollment)
                self.assertEqual(
                    actual,
                    expected
                )


class TestFitnessEvaluation(unittest.TestCase):
    def test_fitness(self):
        test_schedule = {
            "SLA191A": {"time": "10 AM", "room": "Beach 201", "facilitator": "Uther"},
            "SLA201": {"time": "10 AM", "room": "Roman 201", "facilitator": "Glen"},
            "SLA303": {"time": "10 AM", "room": "Beach 301", "facilitator": "Shaw"},
            "SLA291": {"time": "11 AM", "room": "Roman 216", "facilitator": "Uther"},
            "SLA304": {"time": "12 PM", "room": "Roman 201", "facilitator": "Uther"},
            "SLA394": {"time": "12 PM", "room": "Frank 119", "facilitator": "Singer"},
            "SLA451": {"time": "12 PM", "room": "Roman 201", "facilitator": "Numen"},
            "SLA101A": {"time": "1 PM", "room": "Loft 310", "facilitator": "Uther"},
            "SLA191B": {"time": "1 PM", "room": "Loft 310", "facilitator": "Lock"},
            "SLA101B": {"time": "3 PM", "room": "Roman 201", "facilitator": "Zeldin"},
            "SLA449": {"time": "3 PM", "room": "Beach 301", "facilitator": "Tyler"}
        }

        for activity in test_schedule:
            actual = fitness.fitness(test_schedule)
            expected = 2.5
            self.assertEqual(
                actual,
                expected
            )


class TestFacilitatorPreference(unittest.TestCase):
    def test_fac_pref(self):
        test_cases = [
            ("Banks", "SLA101A", data.pref_facil, data.alt_facil, 0.5), # Overseen by preferred facilitator
            ("Numen", "SLA101A", data.pref_facil, data.alt_facil, 0.2), # Overseen by Alternative Facilitator
            ("Uther", "SLA101A", data.pref_facil, data.alt_facil, -0.1) # Overseen by Other Facilitator
        ]
        for fac, act, pref_facil, alt_facil, expected in test_cases:
            with self.subTest(fac=fac, act=act):
                actual = fitness.facil_pref(fac, act, pref_facil, alt_facil)
                self.assertEqual(actual, expected)


class TestTimeOverlap(unittest.TestCase):
    def test_time_overlap(self):
        fac_sched = {
            "Uther": {"times": {"10 AM", "11 AM"}, "acts": ["10 AM", "11 AM"]},
            "Shaw": {"times": {"10 AM"}, "acts": ["10 AM", "10 AM"]},
        }
        actual = fitness.time_overlap(fac_sched)
        expected = [0.2, 0.2, -0.2]  # Reward for single activity, penalty for overlap
        self.assertEqual(actual, expected)


class TestFacOversched(unittest.TestCase):
    def test_fac_oversched(self):
        test_cases = [
            (
                {"Glen": {"count": 0}},  # 0 activities, penalized
                [-0.4]
            ),
            (
                {"Glen": {"count": 1}},  # 1 activity, penalized
                [-0.4]
            ),
            (
                {"Glen": {"count": 2}},  # 2 activities, penalized
                [-0.4]
            ),
            (
                {"Glen": {"count": 3}},  # 3 activities, no penalty
                [0]
            ),
            (
                {"Glen": {"count": 4}},  # 4 activities, no penalty
                [0]
            ),
            (
                {"Glen": {"count": 5}},  # 5 activities, penalized
                [-0.5]
            ),
            (
                {"Tyler": {"count": 0}},  # Tyler, 0 activities, no penalty
                [0]
            ),
            (
                {"Tyler": {"count": 4}},  # Tyler, 4 activities, no penalty
                [0]
            ),
            (
                {"Tyler": {"count": 5}},  # Tyler, 5 activities, penalized
                [-0.5]
            ),
            (
                {
                    "Glen": {"count": 5},
                    "Tyler": {"count": 2},
                    "Uther": {"count": 0},
                    "Banks": {"count": 3}
                },  # Mixed case
                [-0.5, 0, -0.4, 0]
            ),
        ]

        for fac_sched, expected in test_cases:
            with self.subTest(fac_sched=fac_sched):
                actual = fitness.fac_oversched(fac_sched)
                self.assertEqual(actual, expected)


class TestSLASpecificRules(unittest.TestCase):
    def test_specific_rules(self):
        # Define test cases
        test_cases = [
            # Test Case 1: Same activity group at the same time, specific for SLA101
            {
                "filtered_activities": ["SLA101A", "SLA101B"],
                "filtered_rooms": ["Beach 201", "Beach 301"],
                "filtered_times": ["10 AM", "10 AM"],  # Same time
                "expected": [-0.5],  # Penalty for same group at the same time
                "expected_debug": [
                    {
                        "pair": ("SLA101A", "SLA101B"),
                        "same": True,
                        "alt": False,
                        "time_diff": 0,
                    }
                ],
            },
            # Test Case 2: Same activity group at the same time, specific for SLA191
            {
                "filtered_activities": ["SLA191A", "SLA191B"],
                "filtered_rooms": ["Beach 201", "Beach 301"],
                "filtered_times": ["10 AM", "10 AM"],  # Same time
                "expected": [-0.5],  # Penalty for same group at the same time
                "expected_debug": [
                    {
                        "pair": ("SLA191A", "SLA191B"),
                        "same": True,
                        "alt": False,
                        "time_diff": 0,
                    }
                ],
            },
            # Test Case 3: Same activity group widely spaced apart, specifc for SLA101
            {
                "filtered_activities": ["SLA101A", "SLA101B"],
                "filtered_rooms": ["Beach 201", "Roman 216"],
                "filtered_times": ["10 AM", "3 PM"],  # 5 hours apart
                "expected": [0.5],  # Reward for same group widely spaced apart
                "expected_debug": [
                    {
                        "pair": ("SLA101A", "SLA101B"),
                        "same": True,
                        "alt": False,
                        "time_diff": 5,
                    }
                ],
            },
            # Test Case 4: Same activity group widely spaced apart, specifc for SLA191
            {
                "filtered_activities": ["SLA191A", "SLA191B"],
                "filtered_rooms": ["Beach 201", "Roman 216"],
                "filtered_times": ["10 AM", "3 PM"],  # 5 hours apart
                "expected": [0.5],  # Reward for same group widely spaced apart
                "expected_debug": [
                    {
                        "pair": ("SLA191A", "SLA191B"),
                        "same": True,
                        "alt": False,
                        "time_diff": 5,
                    }
                ],
            },
            # Test Case 5: alt SLA101 and SLA191 in consecutive time slots, no Roman_Beach penalty
            {
                "filtered_activities": ["SLA101A", "SLA191A"],
                "filtered_rooms": ["Beach 201", "Beach 301"],
                "filtered_times": ["10 AM", "11 AM"],  # Consecutive times
                "expected": [0.5],  # Reward for alt activities in consecutive slots w/o Roman/Beach Penalty
                "expected_debug": [
                    {
                        "pair": ("SLA101A", "SLA191A"),
                        "same": False,
                        "alt": True,
                        "time_diff": 1,
                    }
                ],
            },
            # Test Case 6: alt SLA101 and SLA191 in consecutive time slots, with Roman/Beach penalty
            {
                "filtered_activities": ["SLA101A", "SLA191A"],
                "filtered_rooms": ["Beach 201", "Loft 206"],
                "filtered_times": ["10 AM", "11 AM"],  # Consecutive times
                "expected": [0.1],  # Reward for alt activities in consecutive slots w/ Roman/Beach Room Penalty
                "expected_debug": [
                    {
                        "pair": ("SLA101A", "SLA191A"),
                        "same": False,
                        "alt": True,
                        "time_diff": 1,
                    }
                ],
            },
            # Test Case 7: alt SLA101 and SLA191 activities one hour apart
            {
                "filtered_activities": ["SLA101A", "SLA191A"],
                "filtered_rooms": ["Beach 201", "Roman 216"],
                "filtered_times": ["10 AM", "12 PM"],  # 2 hours apart
                "expected": [0.25],  # Reward for alt activities one hour apart
                "expected_debug": [
                    {
                        "pair": ("SLA101A", "SLA191A"),
                        "same": False,
                        "alt": True,
                        "time_diff": 2,
                    }
                ],
            },
            # Test Case 8: Combination of conditions 1
            {
                "filtered_activities": ["SLA101A", "SLA191A", "SLA101B", "SLA191B"],
                "filtered_rooms": ["Beach 201", "Beach 301", "Roman 216", "Roman 201"],
                "filtered_times": ["10 AM", "11 AM", "1 PM", "1 PM"],
                # Penalties: alt Sections in same time
                # Rewards: alt Consecutive, alt w/ time_diff = 2
                "expected": [0.5, 0, 0, 0.25, 0, -0.5],
                "expected_debug": [
                    # Comparisons between every pair (i, j):
                    {"pair": ("SLA101A", "SLA191A"), "same": False, "alt": True, "time_diff": 0},
                    {"pair": ("SLA101A", "SLA101B"), "same": True, "alt": False, "time_diff": 1},
                    {"pair": ("SLA101A", "SLA191B"), "same": False, "alt": True, "time_diff": 2},
                    {"pair": ("SLA191A", "SLA101B"), "same": False, "alt": True, "time_diff": 1},
                    {"pair": ("SLA191A", "SLA191B"), "same": True, "alt": False, "time_diff": 2},
                    {"pair": ("SLA101B", "SLA191B"), "same": False, "alt": True, "time_diff": 1},
                ],   
            },
            # Test Case 9: Combination of conditions 2
            {
                "filtered_activities": ["SLA101A", "SLA101B", "SLA191A", "SLA191B"],
                "filtered_rooms": ["Roman 201", "Beach 301", "Roman 216", "Roman 201"],
                "filtered_times": ["10 AM", "10 AM", "12 PM", "1 PM"],
                # Penalties: SLA101 in same time
                # Rewards: alt w/ time_diff = 2 (x2)
                "expected": [-0.5, 0.25, 0, 0.25, 0, 0],
                "expected_debug": [
                    # Pair comparisons (i, j)
                    {"pair": ("SLA101A", "SLA101B"), "same": True, "alt": False, "time_diff": 0},
                    {"pair": ("SLA101A", "SLA191A"), "same": False, "alt": True, "time_diff": 2},
                    {"pair": ("SLA101A", "SLA191B"), "same": False, "alt": True, "time_diff": 3},
                    {"pair": ("SLA101B", "SLA191A"), "same": False, "alt": True, "time_diff": 2},
                    {"pair": ("SLA101B", "SLA191B"), "same": False, "alt": True, "time_diff": 3},
                    {"pair": ("SLA191A", "SLA191B"), "same": True, "alt": False, "time_diff": 1},
                ],
            },
            # Test Case 10: Combination of conditions 3
            {
                "filtered_activities": ["SLA101A", "SLA191A", "SLA101B", "SLA191B"],
                "filtered_rooms": ["Beach 201", "Beach 301", "Roman 216", "Roman 201"],
                "filtered_times": ["10 AM", "11 AM", "1 PM", "1 PM"],
                # Penalties: alt Sections in same time
                # Rewards: alt Consecutive, alt w/ time_diff = 2
                "expected": [0.5, 0, 0, 0.25, 0, -0.5],
                "expected_debug": [
                    # Pair comparisons (i, j)
                    {"pair": ("SLA101A", "SLA191A"), "same": False, "alt": True, "time_diff": 1},
                    {"pair": ("SLA101A", "SLA101B"), "same": True, "alt": False, "time_diff": 3},
                    {"pair": ("SLA101A", "SLA191B"), "same": False, "alt": True, "time_diff": 3},
                    {"pair": ("SLA191A", "SLA101B"), "same": False, "alt": True, "time_diff": 2},
                    {"pair": ("SLA191A", "SLA191B"), "same": True, "alt": False, "time_diff": 0},
                    {"pair": ("SLA101B", "SLA191B"), "same": False, "alt": True, "time_diff": 0},
                ],
            }
        ]

        # Execute each test case
        for case in test_cases:
            with self.subTest(filtered_activities=case["filtered_activities"]):
                actual_adj, actual_debug = fitness.specific_rules(
                    case["filtered_activities"],
                    case["filtered_rooms"],
                    case["filtered_times"],
                    data.time_cache
                )
                self.assertEqual(actual_adj, case["expected"])
                self.assertEqual(actual_debug, case["expected_debug"])



def load_tests(loader, tests, pattern):
    rb_suite = unittest.TestSuite()
    rb_suite.addTests(loader.loadTestsFromTestCase(TestRomanOrBeach))
    
    consecutive_suite = unittest.TestSuite()
    consecutive_suite.addTests(loader.loadTestsFromTestCase(TestConsecutiveTimeSlots))

    room_suite = unittest.TestSuite()
    room_suite.addTests(loader.loadTestsFromTestCase(TestRoomEvaluation))

    facil_pref_suite = unittest.TestSuite()
    facil_pref_suite.addTests(loader.loadTestsFromTestCase(TestFacilitatorPreference))

    time_overlap_suite = unittest.TestSuite()
    time_overlap_suite.addTests(loader.loadTestsFromTestCase(TestTimeOverlap))

    fitness_suite = unittest.TestSuite()
    fitness_suite.addTests(loader.loadTestsFromTestCase(TestFitnessEvaluation))

    fac_sched_suite = unittest.TestSuite()
    fac_sched_suite.addTests(loader.loadTestsFromTestCase(TestFacOversched))

    specific_rules_suite = unittest.TestSuite()
    specific_rules_suite.addTests(loader.loadTestsFromTestCase(TestSLASpecificRules))

    # Dynamically load tests from all previous suites and isolated test cases.
    master_suite = unittest.TestSuite()
    master_suite.addTests(rb_suite)
    master_suite.addTests(consecutive_suite)
    master_suite.addTests(room_suite)
    master_suite.addTests(facil_pref_suite)
    master_suite.addTests(time_overlap_suite)
    master_suite.addTests(fac_sched_suite)
    master_suite.addTests(specific_rules_suite)
    master_suite.addTests(fitness_suite)
    
    return master_suite


# Run the script
if __name__ == "__main__":
    unittest.main()