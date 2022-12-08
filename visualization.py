import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import covid
import population
import database

def join_tables(cur, conn):
    cur.execute(
        """
        SELECT codes.country_name, covid.country_id, covid.cases, covid.deaths, covid.active, population.under_35, population.over_65, population.total_population
        FROM population
        JOIN covid ON population.country_id = covid.country_id
        JOIN codes ON covid.country_id = codes.id
        
        """
    )

    res = cur.fetchall()
    conn.commit()
    country_list = ['Canada', 'Japan', 'Australia', 'Chile', 'South Africa', 'France']

    final_res = []
    for i in res:
        if i[0] in country_list:
            final_res.append(i)
    return final_res

def over_65(final_res):
    pop = {}

    for i in final_res:
        percentage = i[6]/i[7]
        pop[i[0]] = percentage

    plt.barh((list(pop.keys())), (list(pop.values())))
    plt.title("Percentage of Population Over 65 Per Country")
    plt.ylabel("Country")
    plt.xlabel("Percentage of Population Over 65")
    plt.tight_layout()
    plt.show()

    cases_deaths = {}

    for i in final_res:
        percentage = i[3]/i[2]
        cases_deaths[i[0]] = percentage

    plt.barh((list(cases_deaths.keys())), (list(cases_deaths.values())))
    plt.title("Percentage of COVID-19 Deaths Per Country")
    plt.ylabel("Country")
    plt.xlabel("Percentage of Deaths")
    plt.tight_layout()
    plt.show()
    
    
    return pop, cases_deaths

def under_35(final_res):
    pop = {}

    for i in final_res:
        percentage = i[5]/i[7]
        pop[i[0]] = percentage

    plt.barh((list(pop.keys())), (list(pop.values())))
    plt.title("Percentage of Population Under 35 Per Country")
    plt.ylabel("Country")
    plt.xlabel("Percentage of Population Under 35")
    plt.tight_layout()
    plt.show()


    cases = {}
    for i in final_res:
        percentage = i[2]/i[7]
        cases[i[0]] = percentage

    plt.barh((list(cases.keys())), (list(cases.values())))
    plt.title("Percentage of COVID-19 Cases Per Country")
    plt.ylabel("Country")
    plt.xlabel("Percentage of Cases")
    plt.tight_layout()
    plt.show()
    
    return pop, cases

def write_calc(vis1, vis2):
    calc_dict = {}
    calc_dict['Over 65 Calculations'] = vis1
    calc_dict['Under 35 Calculations'] = vis2

    with open('calculations.txt', 'w') as file:
     file.write(json.dumps(calc_dict))



def main():

    # CREATE TABLES
    # code table
    cur, conn = database.setUpDatabase('database.db')
   
    final_res = join_tables(cur, conn)

    write_calc(over_65(final_res), under_35(final_res))

 
    
if __name__ == "__main__":
    main()

