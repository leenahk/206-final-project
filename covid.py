import json
import os
import requests

def get_covid_data():
    r = requests.get("https://disease.sh/v3/covid-19/countries")
    data = r.text
    covid_data = json.loads(data)

    json_data = json.dumps(covid_data)
    
    with open("covid.json", "w") as outfile:
        outfile.write(json_data)

    # #build new dict with state, cases, deaths, active
    covid_dict = {}
    for country in covid_data:
        temp_dict = {}
        temp_dict["cases"] = country["cases"]
        temp_dict["deaths"] = country["deaths"]
        temp_dict["active"] = country["active"]
        # print(temp_dict)
        covid_dict[country["country"]] = temp_dict
        print(covid_dict)

    

        # covid_dict[country][0] = covid_data[0]["country"]
    
    # print(covid_data[0]["country"])

    
        

def main():
    get_covid_data()

if __name__ == "__main__":
    main()