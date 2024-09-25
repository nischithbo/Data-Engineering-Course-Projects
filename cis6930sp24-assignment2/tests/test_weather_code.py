import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from datahelper import get_weather_code

class TestGetWeatherCode(unittest.TestCase):
    @patch('datahelper.requests.get')
    @patch('datahelper.datetime')
    def test_get_weather_code(self, mock_datetime, mock_requests_get):
        # Mock parameters
        latitude = 40.7128
        longitude = -74.0060
        GMT_time = datetime(2024, 4, 1, 2, 0, 0)  # April 1st, 2024, 3:00 PM

        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "hourly": {
                "weather_code": ["00", "01", "08", "40", "50", "60", "70", "80", "90", "100", "110", "120"]
            }
        }
        mock_requests_get.return_value = mock_response

        # Mock datetime.strftime to return the date and hour
        mock_datetime_obj = MagicMock()
        mock_datetime_obj.strftime.side_effect = ["2024-04-01", "2"]
        mock_datetime.now.return_value = mock_datetime_obj

        # Call the function under test
        weather_code = get_weather_code(latitude, longitude, GMT_time)

        # Verify the output
        self.assertEqual(weather_code, "08")

# Run the tests
if __name__ == "__main__":
    unittest.main()
