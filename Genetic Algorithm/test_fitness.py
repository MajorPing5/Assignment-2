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
    def roman_or_beach_true(self):
        true_cases = [
            ("Roman 216", "Roman 201"),     # Both Roman
            ("Roman 102", "Roman 216"),     # Both Roman, alt variation
            ("Beach 201", "Beach 301"),     # Both Beach
            ("Beach 301", "Beach 201"),     # Both Beach, alt variation
            ("Loft 206", "Frank 119"),      # Neither Roman nor Beach
        ]
        for previous_room, current_room in true_cases:
            with self.subTest(state="Should Return True", previous_room=previous_room, current_room=current_room):
                self.assertTrue(
                    fitness.roman_or_beach(previous_room, current_room),
                    f"Expected True for previous_room={previous_room}, current_room={current_room}"
                )


    def roman_or_beach_false(self):
        false_cases = [
            ("Roman 201", "Loft 206"),  # Only previous room is Roman
            ("Beach 201", "Loft 206"),  # Only previous room is Beach
            ("Loft 206", "Roman 201"),  # Only current room is Roman
            ("Loft 206", "Beach 301"),  # Only current room is Beach
        ]
        for previous_room, current_room in false_cases:
            with self.subTest(state="Should Return False", previous_room=previous_room, current_room=current_room):
                self.assertFalse(
                    fitness.roman_or_beach(previous_room, current_room),
                    f"Expected False for previous_room={previous_room}, current_room={current_room}"
                )
        

# Run the script
if __name__ == "__main__":
    unittest.main()