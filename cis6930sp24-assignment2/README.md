## Name: Nischith Bairannanavara Omprakash

## Project Description 

In this project, we aim to automate the process of acquiring, processing, and analyzing incident reports from the Norman Police Department. Initially, the project involves downloading PDF files containing daily incident details via the department's API. Once acquired, these PDFs are parsed to extract data about each incident, such as the nature of the incident, time, and location. The project then focuses on enriching the dataset with additional contextual details such as the day of the week, time of day, weather conditions, location rank, side of town, incident rank, nature, and EMSSTAT. The project retrieves the latitude and longitude of each address extracted from the PDF and then uses this information to calculate the side of town and obtain weather data. Batch processing is utilized to obtain coordinates for multiple addresses simultaneously and to retrieve weather conditions for each location, reducing processing time. Additionally, the coordinates of unique addresses are stored in a database to avoid repeatedly calling the geocoding API.
## How to install and run

1.Install pyenv and pipenv if not already installed.

2.Install the Python version of your choice using the command "pyenv install {PYTHON_VERSION}".

3.Open the project folder and set the local Python version with "pyenv local {PYTHON_VERSION}".

4.Install SQLite3 for database management by using: "sudo apt install sqlite3".

5.To create a pipenv environment for the project, run "pipenv install".

6.Activate the pipenv environment using the command "pipenv shell".

7.To run test cases and check the application's functionality, enter the command: 'pipenv run python -m pytest'.

8.Execute the application by typing: 'pipenv run python assignment2.py --urls "file"'. Replace file with actual path.

Note: input file should contain urls in separate lines

## Assumptions
1. The starting points of columns in the PDF remain the same, as the x-coordinate is hardcoded for data extraction.
2. Each valid incident must have at least the date/time and incident number mentioned.
3. Historical Weather API is used to get weather code and assumed to return code without throwing errors.
4. Google geocode API is used to latitude and longitude and  assumed to return code without throwing errors.
5. The weather code API is assumed to give weather code based on local time zone of coordinates by setting the timezone parameter to auto.
6. Google geocode API is used and assumed to provided in google_api_key.json and has right permission to execute geocode API.
7. The get_cardinal_direction function calculates the compass direction (e.g., N, NE) from one geographic point to another(for this project the center of town). It does so by determining the angle between the points and mapping this angle to the closest cardinal direction.
8. For EMSSTAT, the code looks for subsequent and previous records having the same time of incident. 

# Bugs
1.Exception handling merely prints the error to sys.stderr and does not address the error itself.

2.As the PDF structure is presumed constant, any deviation from this structure could lead to errors.

3.The file used by pytest for testing data extraction is located in the assignment0/tests folder; deleting this file will cause the test case to fail.

4.The database is located in resources folder and file download occur in the resources folder; if this folder is deleted, it results in an error.

5.Ranking of location and nature is solely based of string extracted from pdf.

6.If API is not able to get weather code the weather coed will be empty string("") in output.

7.If API is not able to fetch geocode or location in pdf is empty or UNKNOWN the side of the town will "" and for calculating weather code will be calculated for center of the town(35.220833, -97.443611).

8.For rounding off time, minutes are excluded.

9.Weather code for any time will be that of the particular hour(ex: weather code for 2/1/2024 6:39 will be that of 2/1/2024 6:00).

10.Input file is assumed to contain urls and each url in separate line. Any deviation from this format will result in failure.

11.If Historical weather API rate limits the system API calls will no return values resulting weather code to be empty.

12.If we are unable to get coordinate for location the side of the town for the location will be empty.

## Functions Description

**assignment2.py**

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

**process_incident_list**

    Processes a list of incident records, enriching each record with additional
    contextual data derived from various calculations and external sources,
    including weather conditions, and prints the augmented data.

    This function augments each incident with the following information:
    - Day of the week and time of day based on the incident's datetime.
    - Weather condition code fetched from an external weather API.
    - Location rank based on the frequency of incident occurrences at various locations.
    - Cardinal direction representing the side of town where the incident occurred.
    - Nature rank based on the frequency of different incident natures.
    - A boolean indicating whether EMSSTAT is related to the incident.
    The augmented data for each incident is printed in a tab-separated format.

    Parameters:
    - incident_list: A list of dictionaries, where each dictionary represents an incident
      record with keys like "location", "Date\\Time", "nature", and "Incident ORI".

    Operations performed on each incident record:
    1. Determine the latitude and longitude for the incident location.
    2. Calculate the rounded-off datetime object for the incident's datetime.
    3. Fetch weather condition codes for each incident based on its datetime and location.
    4. Determine additional information like day of the week, time of day, location rank,
       side of town, nature rank, and whether EMSSTAT is applicable.
    5. Print the augmented incident data and append it to `output_list`.

    Returns:
    - None: The function directly modifies a global variable and prints output,
            without returning any value.

**insert_db**
    Inserts or updates location mappings in the 'location_mapping.db' database.

    For each tuple in `insert_values`, containing (address, latitude, longitude),
    the function inserts a new record into the 'LocationMap' table or updates
    existing records with the same address. Operations are performed within a
    single transaction to ensure atomicity. Errors are printed to stderr.

    Parameters:
    - insert_values: List of tuples (str, float, float) representing (address, lat, lng).

    Returns:
    - None

**get_existing_entries_in_db**
    
    Retrieves all address entries from the 'LocationMap' table in the database.

    Returns a list of tuples, each containing the address, latitude, and longitude
    of a location stored in the 'location_mapping.db' database.

    Returns:
    - addresses: List of tuples (str, float, float) for each entry in the database.


**run**

    Downloads PDFs from provided URLs, extracts incident details, and processes them.

    For each URL in `urls`, this function downloads the corresponding PDF to a
    'resources' directory, extracts incident details (including locations and natures),
    ranks these details, and then augments each incident with additional data such
    as weather conditions and geographical information. It handles errors during
    processing by printing them to stderr.

    Parameters:
    - urls: List of URLs pointing to PDF files containing incident summaries.

    Returns:
    - None

**get_lat_long_for_all_allocation**

    Updates global mapping of addresses to their latitude and longitude coordinates.

    Fetches existing entries from the database to avoid re-geocoding known locations.
    For new locations not in the database, performs batch geocoding and updates the
    database. The global `all_address_to_coordinate` dictionary is then updated with
    the latest coordinates for all addresses.

    Returns:
    - None

**read_urls**

    Reads a list of URLs from a specified file.

    Opens and reads each line of the given file, treating each non-empty line as a URL.
    Any lines that are only whitespace or empty are ignored. If an error occurs during
    file reading, an error message is printed to stderr, and any URLs read up to that
    point are returned.

    Parameters:
    - filename: The path to the file containing URLs, one per line.

    Returns:
    - urls: A list of URLs read from the file. If an error occurs, returns the URLs
            read up to the point of the error.


# datahelper.py
**get_cardinal_direction**

    Calculates the cardinal direction from a start point to an end point.

    Determines the cardinal direction (e.g., N, NE, E, SE, S, SW, W, NW) based on the
    geographic coordinates of the start and end points. If the start and end points
    are the same, returns an empty string. Uses forward azimuth calculation to
    determine the direction.

    Parameters:
    - start_lat (float): Latitude of the start point.
    - start_lng (float): Longitude of the start point.
    - end_lat (float): Latitude of the end point.
    - end_lng (float): Longitude of the end point.

    Returns:
    - cardinal_direction (str): The cardinal direction from the start point to the
      end point. Returns an empty string if an error occurs or if the start and end
      points are the same.

**get_place_coordinate**
    
    Attempts to geocode a given address into latitude and longitude coordinates.

    This function makes use of the Google Maps Geocoding API to convert addresses
    into geographic coordinates. If the address is already in a coordinate format
    (latitude;longitude), it returns these values directly. It retries the request
    up to a specified number of times if it encounters timeouts or API rate limits.

    Parameters:
    - api_key (str): The API key for accessing the Google Maps Geocoding API.
    - address (str): The address to geocode, or a string in "lat;lng" format.
    - attempts (int): The maximum number of attempts to make in case of errors
                      or API rate limits (default is 3).

    Returns:
    - tuple: A tuple containing the original address and a tuple of the geocoded
             latitude and longitude (as strings). If geocoding fails, returns
             the address with empty string values for latitude and longitude.

    Note:
    - The function waits increasingly longer between retries if the API rate limit
      is exceeded. For other errors, such as timeouts, it waits a fixed amount of time.
    - If all attempts fail, or if an unexpected error occurs, it returns the address
      with empty strings for the coordinates.

**batch_geocode**
    
    Geocodes a list of addresses in parallel, using multiple threads.

    Utilizes a thread pool to concurrently request geographic coordinates for
    each address in the input list. It relies on the `get_place_coordinate`
    function for the actual geocoding process.

    Parameters:
    - api_key (str): API key for the geocoding service.
    - addresses (list of str): A list of addresses to geocode.

    Returns:
    - results (list of tuples): A list where each tuple contains the original address
      and its geocoded latitude and longitude. If geocoding fails, latitude and longitude
      are returned as empty strings.

**batch_weather_code**
    
    Retrieves weather codes for multiple locations concurrently using threads.

    This function uses a thread pool to make parallel requests for weather codes based on
    the geographic coordinates of each location. It utilizes the `get_weather_code` function
    to fetch the weather condition code for each specified time and location.

    Parameters:
    - location_details (dict): A dictionary where each key is an index representing a unique
      location, and the value is a tuple containing the location's details, including latitude,
      longitude, and the time for which the weather code is requested.

    Returns:
    - results (dict): A dictionary mapping each location index to its corresponding weather
      code. If an error occurs during the retrieval process for a location, its value is set
      to an empty string.

**get_weather_code**
    
    Fetches the weather code for a specific location and time from an API.

    Attempts to retrieve the weather condition code using the Open-Meteo API by specifying
    the latitude, longitude, and date/time. It retries the request a few times in case of
    failures like timeouts or server errors.

    Parameters:
    - latitude (float): The latitude of the location.
    - longitude (float): The longitude of the location.
    - time (datetime): The datetime object representing when the weather code is requested.

    Returns:
    - str: A formatted weather code as a string. Returns an empty string if the request fails
      or if no code is available for the specified time.

**get_hour**
    
    Extracts the hour from a datetime object as a string in 24-hour format.
    
    Parameters:
    - datetime_obj (datetime): The datetime object from which to extract the hour.
    
    Returns:
    - str: The hour extracted from `datetime_obj`, formatted as a two-digit string.

**get_round_off_hour_and_datetime_obj**
    
    Rounds off a datetime object to the nearest hour, removing minutes and seconds.
    
    Parameters:
    - date_time_obj (datetime): The datetime object to round off.
    
    Returns:
    - datetime: A new datetime object rounded to the nearest hour.

**get_day_of_week_code**

    Converts a datetime object to a custom day-of-week code.
    
    Transforms the ISO day of the week (where Monday is 1 and Sunday is 7) to a custom
    numbering system where Sunday is 1 and Saturday is 7.
    
    Parameters:
    - datetime_obj (datetime): The datetime object for which to calculate the day-of-week code.
    
    Returns:
    - int: The custom day-of-week code, ranging from 1 (Sunday) to 7 (Saturday).

**rank_items**
    
    Assigns rankings to items based on their frequency in the provided list.
    
    This function counts the occurrences of each item in the list, sorts the items
    by their frequency (highest first), and then assigns rankings starting from 1.
    Ties in frequency result in the same rank. Items with the same frequency as the
    previous item receive the same rank. An empty string, if present, is assigned
    the last rank.
    
    Parameters:
    - item_list (list): The list of items to rank.
    
    Returns:
    - dict: A dictionary where keys are items and values are lists containing
            the item's rank and its frequency in the provided list.

# tests/test_run.py

**test_download_incident_summary_file**

	 Tests the download_incident_summary_file function to ensure it correctly downloads a file from a given URL and saves it to the specified path. It mocks the network call to urlopen and verifies:
    - The correct URL is called.
    - The file is saved in the correct directory with the correct content.

**test_data_extraction**

	 Tests the extract_incident_details_from_pdf function to ensure it correctly extracts incident data from a PDF file. It verifies that the returned list of incidents matches the expected data structure and values.
	 

# test/test_geocode.py

**TestGetPlaceCoordinate**

    Unit tests for the `get_place_coordinate` function in the `datahelper` module.
    
    Tests the functionality of `get_place_coordinate` by using mock responses from
    the requests to simulate API calls. It verifies that the function correctly
    parses and returns the latitude and longitude coordinates for both standard
    addresses and coordinates passed as strings.

    Methods:
    - test_get_place_coordinate: Tests that the function returns the expected 
      tuple of address and coordinates (lat, lng) for given inputs. Uses patching
      to mock the `requests.get` method call, simulating API responses.

# tests/test_utility.py

**test_get_hour**
    
    Verifies that `get_hour` correctly extracts the hour from a datetime object.

**test_get_day_of_week_code**

    Tests `get_day_of_week_code` for accuracy against known day-of-week codes,
    ensuring Monday returns 2 and Sunday returns 1 under the custom numbering system.

**test_rank_items**
    
    Checks `rank_items` for correct item ranking based on frequency within a list,
    including proper handling of ties and assignment of rank for an empty string.

# tests/test_weather_code.py
    
    Unit tests for the `get_weather_code` function in the `datahelper` module.
    
    This test case mocks external dependencies, including the requests library
    and datetime module, to test the functionality of `get_weather_code`. It
    ensures that the function correctly processes input parameters, makes the
    appropriate API call, and accurately extracts the weather code from the
    API response based on the specified time.
    
    Methods:
    - test_get_weather_code: Verifies that `get_weather_code` returns the expected
      weather code for a given latitude, longitude, and datetime. Mocks API responses
      and the current time to test various scenarios.

