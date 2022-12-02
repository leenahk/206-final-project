import json
import os
import requests
import csv

def get_population_data():

    # request data from API -- https://api.census.gov/data/timeseries/idb/1year?get=NAME,AGE,POP,AREA_KM2&GENC=&YR=2021
    x = 'FPOP65_69,FPOP70_74,FPOP75_79,FPOP80_84,FPOP85_89,FPOP90_94,FPOP95_99,MPOP65_69,MPOP70_74,MPOP75_79,MPOP80_84,MPOP85_89,MPOP90_94,MPOP95_99,'
    resp = requests.get('https://api.census.gov/data/timeseries/idb/5year?get=NAME,POP,CBR,CDR,E0,AREA_KM2,'+x+'GENC&YR=2021')
    data = resp.text
    pop_data = json.loads(data)
    
    # write population data file
    with open("population_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(pop_data)

    # read population data file
    file = open('population_data.csv', 'r')
    content = file.readlines()
    file.close()


    pop_list = []
    
    for i in content[1:]:
        pop_dict = {}
        over_65 = 0

        country = i.split(',')[0]
        total_pop = i.split(',')[1]
        j = i.split(',')[6:20]
        
        for j in i.split(',')[6:20]:
            over_65 += float(j)
        
        pop_dict['country'] = country
        pop_dict['over_65'] = over_65
        pop_dict['total_population'] = total_pop
        
        pop_list.append(pop_dict)

    return pop_list



def main():
   get_population_data()

if __name__ == "__main__":
    main()