import unittest
from datetime import datetime
from datahelper import get_hour, get_day_of_week_code, rank_items

def test_get_hour():
    # Create a datetime object for testing
    datetime_obj = datetime(2024, 4, 1, 15, 30, 45)  # April 1st, 2024, 3:30:45 PM

    # Call the function under test
    hour_str = get_hour(datetime_obj)

    # Verify the output
    assert hour_str == "15"

def test_get_day_of_week_code():
    # Create a datetime object for testing (Monday: 1, Sunday: 7)
    datetime_obj_monday = datetime(2024, 4, 1)  # April 1st, 2024 (Monday)
    datetime_obj_sunday = datetime(2024, 4, 7)  # April 7th, 2024 (Sunday)

    # Call the function under test
    day_of_week_code_monday = get_day_of_week_code(datetime_obj_monday)
    day_of_week_code_sunday = get_day_of_week_code(datetime_obj_sunday)

    # Verify the output
    assert day_of_week_code_monday == 2 # Monday should have code 1
    assert day_of_week_code_sunday == 1  # Sunday should have code 7
#
def test_rank_items():
    # Define sample item list
    item_list = ["apple", "banana", "apple", "banana", "banana", "orange"]

    # Mock the expected return value
    expected_rankings = {
        "banana": [1, 3],  # Rank 1, count 3
        "apple": [2, 2],   # Rank 2, count 2
        "orange": [3, 1],  # Rank 3, count 1
        "": [4, 0]         # Rank 4, count 0 for empty string
    }

    # Call the function under test
    ranking = rank_items(item_list)
    for each in ranking:
        assert expected_rankings[each][0] == ranking[each][0]


# Run the tests
if __name__ == "__main__":
    unittest.main()
