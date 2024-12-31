# test_fitness.py
from test_framework import test_case, test_framework

# Assuming `fitness.py` has functions to calculate fitness, e.g., `calculate_fitness`

@test_case
def test_fitness_perfect_match():
    schedule = { 
        "activity": "SLA101A",
        "room": "Roman 201",
        "time": "10 AM",
        "facilitator": "Glen",
        "expected_enrollment": 50
    }
    score = calculate_fitness(schedule)  # Example function from `fitness.py`
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
    score = calculate_fitness(schedule)
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
    score = calculate_fitness(schedule)
    assert score < 0, "Fitness score should decrease for non-preferred facilitators."

# Run all test cases
if __name__ == "__main__":
    test_framework.run()
