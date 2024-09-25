from datahelper import get_place_coordinate
import pytest
from time import sleep
# Import the function to be tested
from datahelper import get_place_coordinate

import unittest
from unittest.mock import patch

# Import the function to be tested
from datahelper import get_place_coordinate

# Mock sample addresses
ADDRESS_1 = "1600 Amphitheatre Parkway, Mountain View, CA"
ADDRESS_2 = "35.6895:-139.6917"

# Mock response data
response_data_1 = {
    "status": "OK",
    "results": [
        {
            "geometry": {
                "location": {
                    "lat": 37.4220576,
                    "lng": -122.0840897
                }
            }
        }
    ]
}

response_data_2 = {
    "status": "OK",
    "results": [
        {
            "geometry": {
                "location": {
                    "lat": 35.6895,
                    "lng": 139.6917
                }
            }
        }
    ]
}


# Pytest function to test get_place_coordinate function
class TestGetPlaceCoordinate(unittest.TestCase):
    @patch('datahelper.requests.get')
    def test_get_place_coordinate(self, mock_get):
        # Configure the mock response
        mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: response_data_1),
            unittest.mock.Mock(json=lambda: response_data_2)
        ]

        # Define the expected outputs
        expected_output_1 = (ADDRESS_1, (37.4220576, -122.0840897))
        expected_output_2 = (ADDRESS_2, (35.6895, 139.6917))

        # Call the function under test
        output_1 = get_place_coordinate("", ADDRESS_1)
        output_2 = get_place_coordinate("", ADDRESS_2)

        # Verify the outputs
        self.assertEqual(output_1, expected_output_1)
        self.assertEqual(output_2, expected_output_2)

# Run the tests
if __name__ == "__main__":
    unittest.main()
