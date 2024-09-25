## Name: Nischith Bairannanavara Omprakash

## Project Description 
In this project, we aim to automate the process of acquiring, processing, and analyzing incident reports from the Norman Police Department. Initially, the project involves downloading PDF files containing daily incident details via the department's API. Once acquired, these PDFs are parsed to extract data about each incident, such as the nature of the incident, time, and location. This extracted information is then systematically stored in a database, designed to facilitate efficient data management and retrieval. The final component of the project involves querying this database to compile statistics on the frequency of each type of incident, categorized by its nature.

## How to install and run

1.Install pyenv and pipenv if not already installed.

2.Install the Python version of your choice using the command "pyenv install {PYTHON_VERSION}".

3.Open the project folder and set the local Python version with "pyenv local {PYTHON_VERSION}".

4.Install SQLite3 for database management by using: "sudo apt install sqlite3".

5.To create a pipenv environment for the project, run "pipenv install".

6.Activate the pipenv environment using the command "pipenv shell".

7.To run test cases and check the application's functionality, enter the command: 'pipenv run python -m pytest'.

8.Execute the application by typing: 'pipenv run python assignment0/main.py --incidents <url>'. Replace <url> with the specific URL for the incidents.

Video Demonstration link :[Link](https://uflorida-my.sharepoint.com/:v:/g/personal/nischith_bairann_ufl_edu/EV5RCYGoeS1LqcTiDagO1NIBp-sboG6gyiZyUA4q7jQwHA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=mATfp1)

## Functions Description
**assignment0/main.py**

**display_status**

    Executes a query to count and display the frequency of incidents by their nature from the 'incidents' table of normanpd.bd database.
    Results are ordered by frequency in descending order, with empty 'nature' values listed last, and within each frequency group, sorted alphabetically by 'nature'.
    Each row is printed in the format: 'nature|incident_count'.

    :param cursor: Database cursor object used to execute the query.
	
**create_db**

    Creates or resets the 'incidents' table in the SQLite database 'normanpd.db', and populates it with incident data.

    This function first checks if the 'incidents' table already exists in the database. If it does, the table is dropped to reset its contents. Then, it creates a new 'incidents' table with columns for incident time, number, location, nature, and ORI. After creating the table, the function iterates over the provided list of incidents, inserting each incident into the table.

    Parameters:
    - incident_list: A list of dictionaries, where each dictionary represents an incident and its details (Date\\Time, Incident Number, location, nature, and Incident ORI).

    Returns:
    - cursor: The SQLite cursor object used for database operations, which can be used for further queries on the database.

    Note:
    - The database 'normanpd.db' is stored in the 'resources' directory relative to the parent directory of this script.
	
**download_incident_summary_file**

    Downloads an incident summary file from a given URL and saves it to a 'resources' directory.

    This function performs an HTTP GET request to the specified URL to download the file. It then saves the file
    to a directory named 'resources', which is located in the parent directory of the script. If the 'resources'
    directory does not exist, it is created. The file is saved with its original name extracted from the URL.

    Parameters:
    - url: The URL of the incident summary file to download.

    Note:
    - The function assumes the file is a PDF, but it can download any file type as is.
    - The directory structure used for saving the file is determined relative to the script's location.

**extract_incident_details_from_pdf**

	Extracts details of incidents from a PDF file and organizes them into a list of dictionaries.
	It first extrcats all the rows of a page and then within each row it extracts the blocks of the columns and creats a dictionary containing date/time, incident number, location, nature of the incident, and the ORI details of each incidents and creats a list of all incidents.
	There are cases to handle row which do not have incident detials.
	
**run**

     Orchestrates the downloading, extraction, and database insertion of incident data from a PDF file specified by a URL.

    This function performs a series of operations to process incident reports:
    1. Downloads the incident summary PDF file from the given URL.
    2. Extracts incident details from the downloaded PDF file.
    3. Creates or resets a database table and inserts the extracted incident data into it.
    4. Displays the count and nature of incidents sorted by their frequency and alphabetically by nature.
	
	Parameters:
    - url: The URL of the PDF file containing the incident summary to be processed.


# tests/test_run.py

**test_download_incident_summary_file**

	 Tests the download_incident_summary_file function to ensure it correctly downloads a file from a given URL and saves it to the specified path. It mocks the network call to urlopen and verifies:
    - The correct URL is called.
    - The file is saved in the correct directory with the correct content.

**test_data_extraction**

	 Tests the extract_incident_details_from_pdf function to ensure it correctly extracts incident data from a PDF file. It verifies that the returned list of incidents matches the expected data structure and values.
	 
**test_db_creation**

	Tests the create_db function to ensure it correctly creates a SQLite database and the 'incidents' table within it. It verifies the database file is created in the specified location.

**test_db_entry**

	Tests database entries by inserting a sample incident record and then querying the database to ensure the record is correctly inserted and can be retrieved with the expected values.
	


## Assumptions

1. The starting points of columns in the PDF remain the same, as the x-coordinate is hardcoded for data extraction.
2. Each valid incident must have at least the date/time and incident number mentioned.

## Bugs

1.Exception handling merely prints the error to sys.stderr and does not address the error itself.

2.As the PDF structure is presumed constant, any deviation from this structure could lead to errors.

3.The file used by pytest for testing data extraction is located in the assignment0/tests folder; deleting this file will cause the test case to fail.

4.The database creation and file download occur in the resources folder; if this folder is deleted, it results in an error.

