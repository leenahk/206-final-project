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

def create_country_code_table(cur, conn, data):
    country_list = []
    for country in data:
        country_name = country['country']
        if country_name not in country_list:
            country_list.append(country_name)
        
    cur.execute("CREATE TABLE IF NOT EXISTS codes (id INTEGER PRIMARY KEY, country_name TEXT UNIQUE)")
    for i in range(len(country_list)):

        cur.execute("INSERT OR IGNORE INTO codes (id,type) VALUES (?,?)",(i,country_list[i]))

    conn.commit()

def create_covid_table(cur, conn, data):
    cur.execute("CREATE TABLE IF NOT EXISTS covid (country TEXT PRIMARY KEY, cases INTEGER, deaths INTEGER, active INTEGER)")

    for i in data:
        cur.execute('SELECT id from codes where country = ?', (i['country']))
        country_id = int(cur.fetchone()[0])
    
    conn.commit()

def add_country(cur, conn):

    covid_data = covid.get_covid_data()
    for item in covid_data:
        cases = item['cases']
        deaths = item['deaths']
        active = item['active']
       
        cur.execute(
            """
            INSERT OR IGNORE INTO covid (cases, deaths, 
            active)
            VALUES (?, ?, ?, ?)
            """,
            (cases, deaths, active)
        )
    conn.commit()


def create_population_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS population (country TEXT PRIMARY KEY, over_65 INTEGER, total_population INTEGER)")
    conn.commit()

def add_population(cur, conn):

    population_data = population.get_population_data()
    for item in population_data:
        country = item['country']
        over_65 = item['over_65']
        total_population = item['total_population']
       
        cur.execute(
            """
            INSERT OR IGNORE INTO population (country, over_65, total_population)
            VALUES (?, ?, ?)
            """,
            (country, over_65, total_population)
        )
    conn.commit()

def join_tables(cur, conn):
    cur.execute(
        """
        SELECT covid.country, covid.cases, covid.deaths, covid.active, population.over_65, population.total_population
        FROM population
        JOIN covid ON population.country = covid.country
        """
    )

    res = cur.fetchall()
    conn.commit()
    print(res)
    return res
    
        

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('database.db')

    create_country_code_table(cur, conn, population.get_population_data())

    create_covid_table(cur, conn, covid.get_covid_data())
    add_country(cur, conn)

    create_population_table(cur, conn)
    add_population(cur, conn)

    join_tables(cur, conn)

if __name__ == "__main__":
    main()