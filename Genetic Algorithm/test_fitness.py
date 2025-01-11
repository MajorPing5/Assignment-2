# test_fitness.py
from test_framework import test_case, test_framework
from population import generate_random_population

def display_schedule(schedule):
    """Display a single schedule in a readable format."""
    print("Generated Schedule:")
    for time, activities in schedule.items():
        print(f"Time: {time}")
        for activity, details in activities.items():
            print(f"  Activity: {activity}")
            for key, value in details.items():
                print(f"    {key.capitalize()}: {value}")

def generate_and_display_schedule():
    """Generate and display one random schedule."""
    # Generate a single schedule
    schedule = generate_random_population(1)[0]  # Extract the first schedule

    # Display the schedule
    display_schedule(schedule)

    # Pause for manual review
    input("\nPress Enter to close...")

# Run the script
if __name__ == "__main__":
    generate_and_display_schedule()

"""# Assuming `fitness.py` has functions to calculate fitness, e.g., `calculate_fitness`

@test_case
def test_fitness_perfect_match():
    schedule = { 
        "activity": "SLA101A",
        "room": "Roman 201",
        "time": "10 AM",
        "facilitator": "Glen",
        "expected_enrollment": 50
    }
    score = fitness(schedule)  # Example function from `fitness.py`
    assert score > 0, "Fitness score should be positive for perfect match."

@test_case
def test_fitness_room_too_small():
    schedule = {
        "activity": "SLA101A",
        "room": "Slater 003",  # Too small for 50
        "time": "10 AM",
        "facilitator": "Glen",
        "expected_enrollment": 50
    }
    score = fitness(schedule)
    assert score < 0, "Fitness score should be negative for a room too small."

@test_case
def test_fitness_facilitator_not_preferred():
    schedule = {
        "activity": "SLA101A",
        "room": "Roman 201",
        "time": "10 AM",
        "facilitator": "Richards",  # Not preferred for SLA101A
        "expected_enrollment": 50
    }
    score = fitness(schedule)
    assert score < 0, "Fitness score should decrease for non-preferred facilitators."

# Run all test cases
if __name__ == "__main__":
    test_framework.run()"""
