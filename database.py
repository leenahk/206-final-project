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


# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS employees (employee_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, job_id INTEGER, hire_date TEXT, salary NUMERIC)")
    conn.commit()
# ADD EMPLOYEE'S INFORMTION TO THE TABLE
# a list of lists
def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    data = json.loads(file_data)
    for item in data:
        id = item['employee_id']
        f_name = item['first_name']
        l_name = item['last_name']
        date = item['hire_date']
        job = item['job_id']
        sal = item['salary']
        cur.execute(
            """
            INSERT OR IGNORE INTO employees (employee_id, first_name, last_name, 
            job_id, hire_date, salary)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (id, f_name, l_name, job, date, sal)
        )
    conn.commit()

        

def main():
    
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('database.db')

    # create_employee_table(cur, conn)
    # add_employee("employee.json",cur, conn)
    # job_and_hire_date(cur, conn)
    # wrong_salary = (problematic_salary(cur, conn))
    # print(wrong_salary)
    # visualization_salary_data(cur, conn)

if __name__ == "__main__":
    main()