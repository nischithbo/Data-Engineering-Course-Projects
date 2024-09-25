import copy
import assignment1.entityresolver as entity_resolver
import re
import spacy, spacy.cli
import requests
import json
import os

class MaskString:
    def __init__(self, **kwargs):
        self.input_string = None
        self.nlp = spacy.load("en_core_web_md")
        self.doc = None
        self.partially_hidden_string = None
        self.gcp_entities = None

    def set_input_string(self, input_string):
        self.input_string = input_string
        self.doc = self.nlp(input_string)
        self.partially_hidden_string = input_string
        self.gcp_entities = self.gcp_nlp(input_string)

    def gcp_nlp(self, input_string):
        api_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "gcp_api_key",  "google_api_key.json")))
        with open(api_file_path, 'r') as file:
            api_key_data = json.load(file)
            api_key = api_key_data['api_key']
        url = "https://language.googleapis.com/v1/documents:analyzeEntities?key=" + api_key
        headers = {"Content-Type": "application/json"}
        body = {
        "document": {
            "type": "PLAIN_TEXT",
            "content": input_string
        },
        "encodingType": "UTF8"
        }

        response = requests.post(url, headers=headers, json=body)
        entities = response.json().get('entities', [])
        return entities

    def hide(self, hide_list):
        count = 0
        out_string = copy.deepcopy(self.partially_hidden_string)
        for each_string in hide_list:
            regex_pattern = re.escape(each_string).replace(r"\ ", r"\s*")
            try:
                for match in re.finditer(regex_pattern, self.input_string):
                    start_pos = match.start()
                    end_pos = match.end()
                    # print(f"Match : {self.input_string[start_pos: end_pos+1]}")
                    sub = ""
                    inc_count = True
                    for i in range(start_pos, end_pos):
                        if self.input_string[i] != '\n':
                            if inc_count and self.input_string[i] == '\u2588':
                                inc_count = False
                            sub += '\u2588'
                        else:
                            sub += self.input_string[i]
                    if inc_count:
                        count += 1
                    out_string = out_string[:start_pos] + sub + out_string[end_pos:]

            except Exception as err:
                start = 0
                while True:
                    index = self.input_string.find(each_string, start)
                    if index != -1:
                        sub = ""
                        inc_count = True
                        count += 1
                        for i in range(index, index+len(each_string)):
                            if out_string[i] != '\n':
                                if count and out_string[i] == '\u2588':
                                    inc_count = False
                                sub += '\u2588'
                            else:
                                sub += self.input_string[i]
                        if inc_count:
                            count += 1
                        out_string = out_string[:index] + sub + out_string[index+len(each_string):]
                        start = index + 1
                    else:
                        break

        self.partially_hidden_string = out_string
        return count

    def hide_address(self):
        address_list = entity_resolver.find_all_address(self.input_string, self.doc, self.gcp_entities)
        # print(address_list)
        return self.hide(address_list)

    def hide_names(self):
        names = entity_resolver.find_all_names(self.input_string, self.doc, self.gcp_entities)

        # print(names)
        count = self.hide(names)
        count += self.hide(entity_resolver.find_names_in_email(self))
        # print(entity_resolver.find_names_in_email(self))
        return count

    def hide_date(self):
        dates = entity_resolver.find_all_date(self.input_string, self.doc, self.gcp_entities)
        # print(dates)
        return self.hide(dates)

    def hide_phone_numbers(self):
        phone_numbers = entity_resolver.find_all_phone_numbers(self.input_string, self.doc, self.gcp_entities)
        # print(phone_numbers)
        return self.hide(phone_numbers)
