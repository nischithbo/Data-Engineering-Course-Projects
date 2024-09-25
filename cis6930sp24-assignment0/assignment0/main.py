import urllib.request
import argparse
import fitz
import sqlite3
import os
import sys


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

                incident_details_dict = {"Date\\Time": date_time,
                                         "Incident Number": incident_number,
                                         "Incident ORI": ORI,
                                         "location": location,
                                         "nature": nature}

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
        pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        folder_path = os.path.join(pardir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(os.path.join(folder_path, url.split("/")[-1]), "wb") as pdf_file:
            pdf_file.write(data)
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)


def create_db(incident_list):
    try:
        pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        conn = sqlite3.connect(os.path.join(pardir, "resources", "normanpd.db"))
        cursor = conn.cursor()
        table_name = 'incidents'
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        existing_table = cursor.fetchone()

        # If the table exists, drop it
        if existing_table:
            cursor.execute(f"DROP TABLE {table_name}")

        # Create a table
        cursor.execute('''CREATE TABLE incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
        );''')

        for incident in incident_list:
            cursor.execute('INSERT INTO incidents (incident_time, incident_number,\
             incident_location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)',
                           (incident['Date\\Time'].strip(), incident['Incident Number'].strip(), incident['location'].strip(),
                            incident['nature'].strip(), incident['Incident ORI'].strip()))

        conn.commit()
        return cursor
    except Exception as err:
        print(f"Error: {err}", file=sys.stderr)


def display_status(cursor):
    query = f"SELECT nature, COUNT(*) AS incident_count \
    FROM incidents \
    GROUP BY nature \
    ORDER BY incident_count DESC, (CASE WHEN nature = '' THEN 1 ELSE 0 END), nature"
    cursor.execute(query)
    output = cursor.fetchall()
    for nature in output:
         print(f"{nature[0]}|{nature[1]}")


def run(url):
    pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    pdf_file_path = os.path.join(pardir, "resources", url.split("/")[-1])
    download_incident_summary_file(url)
    incident_list = extract_incident_details_from_pdf(pdf_file_path)
    db_connection = create_db(incident_list)
    display_status(db_connection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        run(args.incidents)



