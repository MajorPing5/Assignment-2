# test_fitness.py
import unittest
import fitness
from population import generate_random_population
# from fitness import fitness


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


def load_tests(loader, tests, pattern):
    rb_suite = unittest.TestSuite()
    rb_suite.addTests(loader.loadTestsFromTestCase(TestRomanOrBeach))
    
    consecutive_suite = unittest.TestSuite()
    consecutive_suite.addTests(loader.loadTestsFromTestCase(TestConsecutiveTimeSlots))

    room_suite = unittest.TestSuite()
    room_suite.addTests(loader.loadTestsFromTestCase(TestRoomEvaluation))

    # Dynamically load tests from all previous suites and isolated test cases.
    master_suite = unittest.TestSuite()
    master_suite.addTests(rb_suite)
    master_suite.addTests(consecutive_suite)
    master_suite.addTests(room_suite)
    
    return master_suite


# Run the script
if __name__ == "__main__":
    unittest.main()