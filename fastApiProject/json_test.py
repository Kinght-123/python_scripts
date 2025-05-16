import xmltodict
import json


def json_parse(json_details):
    mvkd = json_details['mvkd']
    pow = json_details['pow']
    pass


with open('plan.json', 'r') as json_file:
    json_data = json.load(json_file)
for json_details in json_data:
    xml_data = json_parse(json_details)
    print(xml_data)
