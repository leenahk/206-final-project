import json
import os
import requests
import population

def get_covid_data():
    r = requests.get("https://disease.sh/v3/covid-19/countries")
    data = r.text
    covid_data = json.loads(data)

    json_data = json.dumps(covid_data)

    # #build new dict with state, cases, deaths, active
    covid_list = []
    for country in covid_data:
        temp_dict = {}
        temp_dict["country"] = country["country"]
        temp_dict["cases"] = country["cases"]
        temp_dict["deaths"] = country["deaths"]
        temp_dict["active"] = country["active"]
        covid_list.append(temp_dict)
    sorted_covid_list = sorted(covid_list, key=lambda x: x['country'])
   
    return sorted_covid_list


def main():
    get_covid_data()

if __name__ == "__main__":
    main()