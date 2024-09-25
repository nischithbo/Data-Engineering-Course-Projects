import re
import pyap
from phonenumbers import PhoneNumberMatcher
from commonregex import CommonRegex


def find_all_address(input_string, doc_obj, gcp_nlp_entities):
    address = find_address_using_pyap(input_string)
    locations = find_location_using_spacy(doc_obj) + find_location_using_gc_nlp(gcp_nlp_entities)
    address = address + locations
    return list(set(address))


def find_location_using_spacy(doc_obj):
    locations = []
    for ent in doc_obj.ents:
        # Check if the entity is a GPE
        if ent.label_ in ["LOC", "GPE"]:
            locations.append(ent.text)
    return locations


def find_location_using_gc_nlp(gcp_nlp_entities):
    locations = []
    for entity in gcp_nlp_entities:
        if entity.get("type", "") == "LOCATION":
            locations.append(entity["name"])
    return locations


def find_address_using_pyap(input_string):
    address_list = []
    address_obj = pyap.parse(input_string, country='US')
    for address in address_obj:
        address_list.append(address.full_address)
    return address_list


def find_all_names(input_string, doc_obj, gcp_nlp_entities):
    names = find_names_using_spacy(doc_obj) + find_name_using_gcp_nlp(gcp_nlp_entities)
    return list(set(names))


def find_names_using_spacy(doc_obj):
    names = []
    for ent in doc_obj.ents:
        # Check if the entity is a GPE
        if ent.label_ in ["PERSON", "ORG"]:
            names.append(ent.text)
    return names


def find_name_using_gcp_nlp(gcp_nlp_entities):
    names = []
    for entity in gcp_nlp_entities:
        if entity.get("type", "") in ["PERSON"]:
            names.append(entity["name"])
    return names


def find_all_date(input_string, doc_obj, gcp_nlp_entities):
    date = find_date_using_spacy(doc_obj) + find_date_using_gcp_nlp(gcp_nlp_entities) + find_date_using_regex(input_string)
    return list(set(date))


def find_date_using_spacy(doc_obj):
    date = []
    for ent in doc_obj.ents:
        # Check if the entity is a GPE
        if ent.label_ in ["DATE"]:
            date.append(ent.text)
    # print(names)
    return list(set(date))


def find_date_using_gcp_nlp(gcp_nlp_entities):
    dates = []
    for entity in gcp_nlp_entities:
        if entity.get("type", "") in ["DATE"]:
            dates.append(entity["name"])
    return dates


def find_all_phone_numbers(input_string, doc_obj, gcp_nlp_entities):
    phone_numbers = find_phone_numbers_using_phone_number_matcher(input_string) + \
                   find_phone_numbers_using_gcp_nlp(gcp_nlp_entities) +\
                   find_phone_numbers_using_regex(input_string)

    return list(set(phone_numbers))


def find_phone_numbers_using_phone_number_matcher(input_string):
    phone_numbers = []
    matches = PhoneNumberMatcher(input_string, "US")
    for match in matches:
        phone_numbers.append(match.raw_string)
    return phone_numbers


def find_phone_numbers_using_regex(input_string):
    phone_number = []
    pattern = r"\s+((?:\+1\s?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4})"
    matches = re.finditer(pattern, input_string)
    for match in matches:
        # print(match.group(0))
        count = 0
        for i in match.group(0):
            if i.isdigit():
                count += 1
        if count == 10:
            phone_number.append(match.group(0).strip())
            continue
        elif 10 < count < 14:
            if "+" in match.group(0):
                phone_number.append(match.group(0).strip())
    return phone_number


def find_phone_numbers_using_gcp_nlp(gcp_nlp_entities):
    phonenumbers = []
    for entity in gcp_nlp_entities:
        if entity.get("type", "") in ["PHONE_NUMBER"]:
            phonenumbers.append(entity["name"])
    return phonenumbers


def find_names_in_email(maskstring_obj):
    prased_text = CommonRegex(maskstring_obj.input_string)
    string = ""
    for email in prased_text.emails:
        for each in re.split(r'[^a-zA-Z]+', email.rsplit(".", 1)[0]):
            string += each+","
    doc = maskstring_obj.nlp(string)
    name_list = []

    for ent in doc.ents:
        if ent.label_ in ["PERSON"]:
            for text in ent.text.split(","):
                name_list.append(text)
    gcp_nlp_entities = maskstring_obj.gcp_nlp(string)
    for entity in gcp_nlp_entities:
        if entity.get("type", "") in ["PERSON"]:
            name_list.append(entity["name"])
    name_list = [string.strip() for string in name_list if string.strip()]

    return list(set(name_list))


def find_date_using_regex(input_string):
    parsed_text = CommonRegex(input_string)
    if parsed_text.dates:
        return parsed_text.dates
    return []


