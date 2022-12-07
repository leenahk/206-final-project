import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import covid
import population

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#creating the country codes table
def create_country_code_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS codes (id INTEGER PRIMARY KEY, country_name TEXT UNIQUE)")
    conn.commit()

#filling in the country codes table
def add_country_code(cur, conn, population_data):
    country_list = []
    for country in population_data:
        country_name = country['country']
        if country_name not in country_list:
            country_list.append(country_name)

    for i in range(len(country_list)):
        cur.execute("INSERT OR IGNORE INTO codes (id,country_name) VALUES (?,?)",(i,country_list[i]))
    
    conn.commit()

#create table with each countries name and covid statistics
def create_covid_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS covid (country_id INTEGER PRIMARY KEY, cases INTEGER, deaths INTEGER, active INTEGER)")
    conn.commit()

#filling in covid statistics table with using country codes
def add_covid_country(cur, conn, covid_data):

    for item in covid_data:
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
            (country_id, cases, deaths, active,)
        )
    conn.commit()


def create_population_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS population (country_id INTEGER PRIMARY KEY, under_35 INTEGER, over_65 INTEGER, total_population INTEGER)")
    conn.commit()

def add_population(cur, conn, population_data):

    for item in population_data:
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

def join_tables(cur, conn):
    cur.execute(
        """
        SELECT covid.country_id, covid.cases, covid.deaths, covid.active, population.under_35, population.over_65, population.total_population
        FROM population
        JOIN covid ON population.country_id = covid.country_id
        """
    )

    res = cur.fetchall()
    conn.commit()
    return res
    
        

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('database.db')
    population_data = population.get_population_data()
    covid_data = covid.get_covid_data()
    
    # CREATE TABLES
    create_country_code_table(cur, conn)
    create_covid_table(cur, conn)
    create_population_table(cur, conn)

    # ADD TO TABLES
    add_country_code(cur, conn, population.get_population_data())
    add_covid_country(cur, conn, covid.get_covid_data())
    add_population(cur, conn, population.get_population_data())

    join_tables(cur, conn)

if __name__ == "__main__":
    main()