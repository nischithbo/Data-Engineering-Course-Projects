import requests
import re
from datetime import datetime, timedelta
from collections import Counter
from geopy.point import Point
from time import sleep
from math import radians, degrees, atan2, cos, sin
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_cardinal_direction(start_lat, start_lng, end_lat, end_lng):
    # Create Point objects for start and end locations
    try:
        if start_lat == end_lat and start_lng == end_lng:
            return ""

        start_point = Point(start_lat, start_lng)
        end_point = Point(end_lat, end_lng)

        # Calculate the forward azimuth between the two points
        # Note: geopy does not directly provide a bearing or azimuth method, so we calculate it manually.
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [start_lat, start_lng, end_lat, end_lng])
        dLon = lon2 - lon1
        x = cos(lat2) * sin(dLon)
        y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(dLon))
        initial_bearing = atan2(x, y)

        # Convert bearing from radians to degrees
        initial_bearing = degrees(initial_bearing)

        # Normalize the bearing
        bearing = (initial_bearing + 360) % 360

        # Convert bearing to cardinal direction
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        cardinal_direction = directions[int(round(bearing / 45)) % 8]
        return cardinal_direction
    except Exception as err:
        return ""


def get_place_coordinate(api_key, address, attempts=3):
    try:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        original_address = address
        pattern = r"^-?\d+(\.\d+)?;-\d+(\.\d+)?"
        for attempt in range(1, attempts+1):
            match = re.match(pattern, address)
            if match:
                lat, lng = address.split(";")
                return address, (lat, lng)

            try:
                geocode_response = requests.get(geocode_url, timeout=60).json()  # 10-second timeout

                if geocode_response['status'] == 'OK':
                    location = geocode_response['results'][0]['geometry']['location']
                    return original_address, (location['lat'], location['lng'])
                elif geocode_response['status'] == 'OVER_QUERY_LIMIT':
                    # print("API rate limit exceeded. Retrying...")
                    sleep(40*attempt)
                else:
                    # print(f"Error geocoding {address}: {geocode_response['status']}")
                    return address, ("", "")
            except requests.exceptions.Timeout:
                # print(f"Request timed out for {address}. Retrying...")
                sleep(60)
            except requests.exceptions.RequestException as e:
                # Catch other requests-related errors
                # print(f"Request exception for {address}: {e}")
                return address, ("", "")
        # After all attempts
        # print(f"Final : Failed to geocode {address} after {attempts} attempts.")
        return address, ("", "")
    except Exception as err:
        return address, ("", "")


def batch_geocode(api_key, addresses):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_address = {executor.submit(get_place_coordinate, api_key, address): address for address in addresses}

        for future in as_completed(future_to_address):
            address = future_to_address[future]
            try:
                _, coords = future.result()
                results.append((address, coords[0], coords[1]))
            except Exception as exc:
                print(f'{address} generated an exception: {exc}')
                results.append((address, "", ""))
    return results


def batch_weather_code(location_details):
    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_address = {executor.submit(get_weather_code, location_details[index][1], location_details[index][2], location_details[index][4]): location_details[index][0] for index in location_details}

        for future in as_completed(future_to_address):
            index = future_to_address[future]
            try:
                weather_code = future.result()
                results[index] = weather_code
            except Exception as exc:
                print(f'{index} generated an exception: {exc}')
                results[index] = ""
    return results


def get_weather_code(latitude, longitude, time):
    try:
        date = time.strftime("%Y-%m-%d")
        params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date,
        "end_date": date,
        "hourly": "weather_code",
        "User-Agent": "DEA2-44",
        "timezone": "auto"
        }
        url = f"https://archive-api.open-meteo.com/v1/archive"
        hr = int(time.strftime("%H"))

        # Number of retries
        retries = 3
        # Delay between retries in seconds
        retry_delay = 60
        data = None
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # This checks for HTTP errors

                data = response.json()
                if data['hourly']['weather_code']:
                    weather_code = data['hourly']['weather_code'][hr]
                    # Format weather code
                    return f"{int(weather_code):02d}" if 0 <= int(weather_code) <= 99 else str(weather_code)
                #print(data)
                return ""
            except requests.RequestException as e:
                #print(e, data)
                if attempt < retries - 1 and (e.response is None or e.response.status_code >= 500):
                    sleep(retry_delay)  # Wait before retrying
                    continue  # Retry the request
                return ""
    except Exception as err:
        return ""
#
# def get_weather_code(latitude, longitude, GMT_time):
#     # URL for the Open-Meteo Archive API
#     date = GMT_time.strftime("%Y-%m-%d")
#     url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={date}&end_date={date}&hourly=weather_code"
#     hr = int(GMT_time.strftime("%H"))
#
#     try:
#         # Make the request to the Open-Meteo Archive API
#         response = requests.get(url)
#         response.raise_for_status()  # Ensure the request was successful
#
#         # Parse the JSON response
#         data = response.json()
#         if data.get('hourly', {}).get('weather_code'):
#             if 0 <= data['hourly']['weather_code'][hr] <= 9:
#                 return "0" + str(data['hourly']['weather_code'][hr])
#             else:
#                 return str(data['hourly']['weather_code'][hr])
#         return ""
#     except requests.RequestException as e:
#         return ""


def get_date_time_obj(time_str):
    input_format = "%m/%d/%Y %H:%M"
    try:
        input_time = datetime.strptime(time_str, input_format)
        return input_time
    except ValueError as e:
        return None, f"Error parsing time: {e}"


def get_hour(datetime_obj):
    return datetime_obj.strftime("%H")


def get_round_off_hour_and_datetime_obj(date_time_obj):
    return date_time_obj.replace(minute=0, second=0, microsecond=0)

#
# def convert_gmt_minus_5_to_gmt(date_time_obj):
#     gmt_time = date_time_obj + timedelta(hours=5)
#     return gmt_time

#
# def round_to_nearest_hour(time_obj):
#     # If minutes >= 30, round up to the next hour; otherwise, keep the hour as is
#     # check round off
#     if time_obj.minute >= 30:
#         return time_obj + timedelta(hours=1) - timedelta(minutes=time_obj.minute, seconds=time_obj.second, microseconds=time_obj.microsecond)
#     else:
#         return time_obj - timedelta(minutes=time_obj.minute, seconds=time_obj.second, microseconds=time_obj.microsecond)


def get_day_of_week_code(datetime_obj):
    numeric_day_of_week_iso = datetime_obj.isoweekday()
    numeric_day_of_week_custom = numeric_day_of_week_iso % 7 + 1
    return numeric_day_of_week_custom


def rank_items(item_list):
    filtered_list = item_list
    # Count the frequency of each location
    counts = Counter(filtered_list)
    # Sort locations by frequency (most common first)
    sorted_locations = counts.most_common()
    # print(sorted_locations)

    # Assign rankings
    rankings = {}
    rank = 0
    for i, ((item, count)) in enumerate(sorted_locations):
        # If it's the first location or has a different count than the previous, assign new rank
        if i == 0 or count < sorted_locations[i-1][1]:
            rank = i + 1
        rankings[item] = [rank, count]

    # check how to handle empty string
    if "" in item_list:
        rankings[""] = [rank+1, item_list.count("")]

    return rankings



