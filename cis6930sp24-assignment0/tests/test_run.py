import os
import assignment0.main as main
import pytest, sqlite3
from unittest.mock import patch, MagicMock
@pytest.fixture
def mock_urlopen():
	with patch('urllib.request.urlopen') as mock:
		yield mock


def test_download_incident_summary_file(mock_urlopen):
	url = "https://nornam/Dummy_daily_incident_summary.pdf"
	dummy_data = b"Adding test data"

	# Configure the mock to return the fake data
	mock_response = MagicMock()
	mock_response.read.return_value = dummy_data
	mock_urlopen.return_value = mock_response

	# Run the function
	main.download_incident_summary_file(url)

	# Check that urlopen was called with the correct URL
	mock_urlopen.assert_called_once_with(url)
	# Check that the folder and file were created with the correct names
	folder_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'resources')
	assert os.path.exists(folder_path)
	file_path = os.path.join(folder_path, "Dummy_daily_incident_summary.pdf")
	assert os.path.exists(file_path)

	# Check that the file content is correct
	with open(file_path, "rb") as pdf_file:
		assert pdf_file.read() == dummy_data
	pdf_file.close()


def test_data_extraction():
	pdf_path = os.path.join(os.path.dirname(__file__), "2023-12-23_daily_incident_summary.pdf")
	incidents = main.extract_incident_details_from_pdf(pdf_path)
	assert incidents[0] == {'Date\\Time': '12/23/2023 0:07', 'Incident Number': '2023-00086367',
	                        'Incident ORI': 'OK0140200', 'location': '2000 ANN BRANDEN BLVD',
	                        'nature': 'Escort/Transport'}


def test_db_creation():
	incident_list = [{'Date\\Time': '12/23/2023 0:07', 'Incident Number': '2023-00086367', 'Incident ORI': 'OK0140200',
	                  'location': '2000 ANN BRANDEN BLVD', 'nature': 'Escort/Transport'}]
	main.create_db(incident_list)
	folder_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'resources')
	db_path = os.path.join(folder_path, "normanpd.db")
	assert os.path.exists(db_path)


def test_db_entry():
	query = f"SELECT nature, COUNT(*) AS incident_count \
	FROM incidents \
	GROUP BY nature \
	ORDER BY incident_count DESC, nature;"
	folder_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'resources',
	                           'normanpd.db')

	conn = sqlite3.connect(folder_path)
	cursor = conn.cursor()
	cursor.execute(query)
	output = cursor.fetchall()
	assert output == [('Escort/Transport', 1)]


