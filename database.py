import unittest
import sqlite3
import json
import pickle
import os
import matplotlib.pyplot as plt
import covid
import population

def make_master_list():
    master_country_list = []
    covid_data = covid.get_covid_data()
    population_data = population.get_population_data()
    
    pop_list = []
    for i in population_data:
        pop_list.append(i['country'])

    for i in covid_data:
        if i['country'] in pop_list:
            master_country_list.append(i['country'])

    return master_country_list

def fixed_data(data, master_country_list):
    fixed_data = []
    index = 0
    for i in data:
        if i['country'] in master_country_list:
            if index < 194:
                if data[index]['country'] != data[index+1]['country']:
                    fixed_data.append(i)
        index += 1
    return fixed_data


# Create Database
def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#creating the country codes table
def create_country_code_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS codes (id INTEGER PRIMARY KEY, country_name TEXT UNIQUE)")
    conn.commit()

#filling in the country codes table
def add_country_code(cur, conn, data):
    country_list = []
    for country in data:
        country_name = country['country']
        if country_name not in country_list:
            country_list.append(country_name)

    for i in range(len(country_list)):
        cur.execute("INSERT OR IGNORE INTO codes (id,country_name) VALUES (?,?)",(i,country_list[i]))
    
    conn.commit()

#filling in covid statistics table with using country codes
def add_covid_country(cur, conn, start_index, data):

    for item in data[start_index:start_index + 25]:
        cur.execute('SELECT id from codes where country_name = ?', [item['country']])
        
        country_id = (cur.fetchone())

        if country_id != None:
            country_id = country_id[0]
        else:
            continue

        cases = item['cases']
        deaths = item['deaths']
        active = item['active']
    
        cur.execute(
            """
            INSERT OR IGNORE INTO covid (country_id, cases, deaths, 
            active)
            VALUES (?, ?, ?, ?)
            """,
            (country_id, cases, deaths, active)
        )
    conn.commit()


def add_population(cur, conn, start_index, data):

    for item in data[start_index:start_index + 25]:
        cur.execute('SELECT id from codes where country_name = ?', [item['country']])
        country_id = (cur.fetchone())
        if country_id != None:
            country_id = country_id[0]
        else:
            continue
        under_35 = item['under_35']
        over_65 = item['over_65']
        total_population = item['total_population']
       
        cur.execute(
            """
            INSERT OR IGNORE INTO population (country_id, under_35, over_65, total_population)
            VALUES (?, ?, ?, ?)
            """,
            (country_id, under_35, over_65, total_population)
        )
    conn.commit()


def main():
    master_list = make_master_list()
    covid_data = covid.get_covid_data()
    population_data = population.get_population_data()
    fixed_covid_data = fixed_data(covid_data, master_list)
    fixed_population_data = fixed_data(population_data, master_list)


    # SETUP DATABASE AND TABLE
    cur, conn = set_up_database('database.db')
    
    # CREATE TABLES
    # code table
    create_country_code_table(cur, conn)
    add_country_code(cur, conn, fixed_covid_data)
    

    # covid table
    cur.execute("CREATE TABLE IF NOT EXISTS covid (country_id INTEGER PRIMARY KEY, cases INTEGER, deaths INTEGER, active INTEGER)")
    cur.execute('SELECT max (country_id) from covid')

    start_index = cur.fetchone()[0]
    
    if start_index == None:
        start_index = 0 

    else:
        start_index += 1
    
    
    add_covid_country(cur, conn, start_index, fixed_covid_data)
    
    # population table
    cur.execute("CREATE TABLE IF NOT EXISTS population (country_id INTEGER PRIMARY KEY, under_35 INTEGER, over_65 INTEGER, total_population INTEGER)")
    cur.execute('SELECT max (country_id) from population')
    
    start_index = cur.fetchone()[0]
    
    if start_index == None:
        start_index = 0 

    else:
        start_index += 1
    
    add_population(cur, conn, start_index, fixed_population_data)

if __name__ == "__main__":
    main()