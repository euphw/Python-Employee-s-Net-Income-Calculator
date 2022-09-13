import mysql.connector
from configparser import ConfigParser
import csv
import re


# create the connection function
def readDBConfig(filename='config.ini', section='mysql'):
    db = {}

    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        print("Error with config.ini file!")

    return db


# connect to database and create the cursor
creds = readDBConfig()
conn = mysql.connector.MySQLConnection(**creds)
cursor = conn.cursor()

# get the results
cursor.execute('select * from employees')
header = ['id', 'first_name', 'last_name', 'email', 'password', 'gross_income', 'fed_tax', 'on_tax', 'cpp', 'ei',
          'net_income']
rows = cursor.fetchall()

# export to csv
with open('emoloyee_db.csv', 'w') as csvfile:
    csv.writer(csvfile).writerow(header)
    for row in rows:
        for i in range(5,):
            row = list(row)
            row[i] = "${:,.2f}".format(row[i])
        csv.writer(csvfile).writerow(row)

# close cursor
cursor.close()
conn.close()
