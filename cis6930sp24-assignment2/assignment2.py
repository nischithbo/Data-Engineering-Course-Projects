import urllib.request
import argparse
import fitz
import os
import sys
import sqlite3
from datahelper import *
import json

api_key = ""


all_incident_list = []
all_location_list = []
all_nature_list = []
all_address_to_coordinate = {}
location_ranking = {}
nature_ranking = {}
output_list = []


def extract_incident_details_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        incident_list = []
        for page_num in range(doc.page_count):
            page = doc[page_num]
            rows = page.get_text("blocks")
            if page_num == 0:
                date_x0 = 52.560001373291016
                incident_number_x0 = 150.86000061035156
                location_x0 = 229.82000732421875
                nature_x0 = 423.1900244140625
                ORI_x0 = 623.8599853515625
                rows.pop(0)

            for row in rows:
                date_time, incident_number, location, nature, ORI = "", "", "", "", ""
                left, top, right, bottom = row[0], row[1], row[2], row[3]
                if len(row[4].strip().split("\n")) < 3:
                    continue
                date_time = page.get_text(clip=fitz.Rect(left, top, incident_number_x0, bottom)).strip().split('\n')[0]
                incident_number = page.get_text(clip=fitz.Rect(incident_number_x0, top, location_x0, bottom)).split('\n')[0]
                for line in page.get_text(clip=fitz.Rect(location_x0, top, nature_x0, bottom)).strip().split('\n'):
                    if not line:
                        continue
                    if location:
                        location += " "
                    location += line
                for line in page.get_text(clip=fitz.Rect(nature_x0, top, ORI_x0, bottom)).strip().split('\n'):
                    if not line:
                        continue
                    if nature:
                        nature += " "
                    nature += line
                ORI = page.get_text(clip=fitz.Rect(ORI_x0, top, right, bottom)).strip()

                incident_details_dict = {"Date\\Time": date_time.strip(),
                                         "Incident Number": incident_number.strip(),
                                         "Incident ORI": ORI.strip(),
                                         "location": location.strip(),
                                         "nature": nature.strip()}

                incident_list.append(incident_details_dict)
                if not location:
                    continue

        doc.close()
        return incident_list
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)


def download_incident_summary_file(url):
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        folder_name = 'resources'
        pardir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        folder_path = os.path.join(pardir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(os.path.join(folder_path, url.split("/")[-1]), "wb") as pdf_file:
            pdf_file.write(data)
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)


def process_incident_list(incident_list):
    global output_list
    weather_code_dict = {}
    for index, value in enumerate(incident_list):
        lat, lng = all_address_to_coordinate.get(value.get("location", ""), (35.220833, -97.443611))
        if not lat and not lng:
            lat, lng = (35.220833, -97.443611)
        date_time_obj = get_date_time_obj(value["Date\\Time"])
        rounded_off_datetime_obj = get_round_off_hour_and_datetime_obj(date_time_obj)
        weather_code_dict[index] = (index, lat, lng, rounded_off_datetime_obj, rounded_off_datetime_obj)
    weather_codes = batch_weather_code(weather_code_dict)
    for index, incident in enumerate(incident_list):
        day_of_the_week = get_day_of_week_code(weather_code_dict[index][3])
        time_of_day = get_hour(weather_code_dict[index][3])
        location_rank = location_ranking.get(incident.get("location", ""))
        nature_rank = nature_ranking.get(incident.get("nature", ""))
        side_of_town = get_cardinal_direction(35.220833, -97.443611, float(weather_code_dict[index][1]), float(weather_code_dict[index][2]))
        nature = incident["nature"]
        EMSSTAT = True if incident["Incident ORI"].lower() == "emsstat" else False
        i = 1
        if not EMSSTAT:
            while index - i >= 0 and incident["Date\\Time"] == incident_list[index-i]["Date\\Time"]:
                if incident["location"] == incident_list[index-i]["location"] and incident_list[index-i]["Incident ORI"].lower() == "emsstat":
                    EMSSTAT = True
                    break
                i += 1
        i = 1
        if not EMSSTAT:
            while index+i < len(incident_list) and incident["Date\\Time"] == incident_list[index+i]["Date\\Time"]:
                if incident["location"] == incident_list[index+i]["location"] and incident_list[index+i]["Incident ORI"].lower() == "emsstat":
                    EMSSTAT = True
                    break
                i += 1
        EMSSTAT = 1 if EMSSTAT else 0
        list_out = [str(day_of_the_week), str(time_of_day), str(weather_codes[index]), str(location_rank[0]),  str(side_of_town), str(nature_rank[0]), str(nature), str(EMSSTAT)]
        output_list.append(list_out)
        print(str(day_of_the_week) + "\t" + str(time_of_day) + "\t" + str(weather_codes[index]) + "\t" +
              str(location_rank[0]) + "\t" + str(side_of_town) + "\t" + str(nature_rank[0]) +
              "\t" + str(nature) + "\t" + str(EMSSTAT))


def insert_db(insert_values):
    try:
        pardir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        conn = sqlite3.connect(os.path.join(pardir, "resources", "location_mapping.db"))
        cursor = conn.cursor()

        for value in insert_values:
            cursor.execute('INSERT INTO LocationMap (address, lat, lng) VALUES (?, ?, ?) ON CONFLICT(address) DO UPDATE SET lat = excluded.lat, lng = excluded.lng;',
                           (value[0], value[1], value[2]))

        conn.commit()
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)


def get_existing_entries_in_db():
    pardir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    conn = sqlite3.connect(os.path.join(pardir, "resources", "location_mapping.db"))
    cursor = conn.cursor()
    query = """
        SELECT address, lat, lng FROM LocationMap;
        """
    cursor.execute(query)
    addresses = cursor.fetchall()
    return addresses
#
# def get_existing_empty_values_in_db():
#     pardir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
#     conn = sqlite3.connect(os.path.join(pardir, "resources", "location_mapping.db"))
#     cursor = conn.cursor()
#     query = """
#         SELECT address, lat, lng FROM LocationMap
#         WHERE lat = '' AND lng = '';
#         """
#     cursor.execute(query)
#     addresses = cursor.fetchall()
#     return addresses


def run(urls):
    global all_nature_list
    global all_location_list
    global nature_ranking
    global location_ranking
    global all_incident_list
    for url in urls:
        pardir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        pdf_file_path = os.path.join(pardir, "resources", url.split("/")[-1])
        download_incident_summary_file(url)
        incident_list = extract_incident_details_from_pdf(pdf_file_path)
        all_incident_list.append(incident_list)
    for incident_list in all_incident_list:
        for incident in incident_list:
            all_location_list.append(incident.get("location", ""))
            all_nature_list.append(incident.get("nature", ""))

    location_ranking = rank_items(all_location_list)
    nature_ranking = rank_items(all_nature_list)
    get_lat_long_for_all_allocation()
    for incident_list in all_incident_list:
        try:
            process_incident_list(incident_list)
        except Exception as err:
            print(f"error while processing incident: {err}", file=sys.stderr)

#
# def clear_all_entry_in_db():
#     pardir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
#     conn = sqlite3.connect(os.path.join(pardir, "resources", "location_mapping.db"))
#     cursor = conn.cursor()
#     delete_query = """
#     DELETE FROM your_table_name;
#     """
#     cursor.execute(delete_query)
#     conn.commit()


def get_lat_long_for_all_allocation():
    try:
        global all_address_to_coordinate
        valid_db_entries = get_existing_entries_in_db()
        additional_locations = set(all_location_list) - set([entry[0] for entry in valid_db_entries])
        additional_locations_coordinates = batch_geocode(api_key, additional_locations)
        insert_db(additional_locations_coordinates)
        updated_db_entries = get_existing_entries_in_db()
        for entry in updated_db_entries:
            all_address_to_coordinate[entry[0]] = (entry[1], entry[2])
    except Exception as err:
        print(f"Error while processing address: {err}", file=sys.stderr)


def read_urls(filename):
    urls = []
    try:
        urls = []
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    urls.append(line.strip())  # Strip newline character and add URL to list
        return urls
    except Exception as err:
        print(f"Unable read input file with error : {err}", file=sys.stderr)
        return urls

    return urls


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", type=str, required=True,
                        help="File path for url of incident reports")

    api_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "gcp_api_key",  "google_api_key.json")))

    with open(api_file_path, 'r') as file:
        api_key_data = json.load(file)
        api_key = api_key_data['api_key']

    args = parser.parse_args()
    urls = []
    if args.urls:
        urls = read_urls(args.urls)

    run(urls)




