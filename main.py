import re
import json
import requests
import unicodedata


COUNTRIES_ABBREVIATION = "https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-abbreviation.json"
BRAZIL_STATES = "https://raw.githubusercontent.com/gcorreaalves/brazil-states-cities-json/master/states.json"
URL_FLAG_COUNTRY_CODE = "https://flagpedia.net/data/flags/ultra/{code}.png"


def strip_accents(string: str) -> str:
    string = unicodedata.normalize("NFD", string)
    string = string.encode("ascii", "ignore")
    string = string.decode("utf-8")

    return string

def generate_country_code_flag_file(data, flag_url, file_name, slug=False):
    results = {}

    for row in data:
        print(row)
        value, key = row.values()

        flag = flag_url.format(
            code=value.lower() if not slug else strip_accents(value).replace(' ', '-')
        )
        value = { 'code': value, 'flag': flag }

        results.update({ key: value })

    results = json.dumps(results, sort_keys=True, indent=4)

    with open(file_name, 'x+') as file:
        file.write(results)


data = requests.get(COUNTRIES_ABBREVIATION).json()
data = json.loads( json.dumps(data, sort_keys=True, indent=4) )
file_name = input('File name: ')+'.json'
generate_country_code_flag_file(data, URL_FLAG_COUNTRY_CODE, file_name)
