import mysql.connector
from configparser import ConfigParser


# create a function to calculate the Federal tax
def calc_fed_tax(gross_income):
    fed_tax_rate1 = 0.15
    fed_tax_rate2 = 0.205
    fed_tax_rate3 = 0.26
    fed_tax_rate4 = 0.29
    fed_tax_rate5 = 0.33
    if gross_income > 50197:
        if gross_income > 100392:
            if gross_income > 155625:
                if gross_income > 221708:
                    # 33% of taxable income over $221,708
                    fed_tax = fed_tax_rate5 * (gross_income - 221708) + (fed_tax_rate4 * 66083) + (
                            fed_tax_rate3 * 55233) + (fed_tax_rate2 * 50195) + (fed_tax_rate1 * 50197)
                else:
                    # 29% on the next $66,083 of taxable income (on the portion of taxable income over 155,625 up to $221,708)
                    fed_tax = fed_tax_rate4 * (gross_income - 155625) + (fed_tax_rate3 * 55233) + (
                            fed_tax_rate2 * 50195) + (fed_tax_rate1 * 50197)
            else:
                # 26% on the next $55,233 of taxable income (on the portion of taxable income over $100,392 up to $155,625)
                fed_tax = fed_tax_rate3 * (gross_income - 100392) + (fed_tax_rate2 * 50195) + (fed_tax_rate1 * 50197)
        else:
            # 20.5% on the next $50,195 of taxable income (on the portion of taxable income over 50,197 up to $100,392)
            fed_tax = fed_tax_rate2 * (gross_income - 50197) + (fed_tax_rate1 * 50197)
    else:
        # 15% on the first $50,197 of taxable income
        fed_tax = fed_tax_rate1 * gross_income
    return fed_tax


# create a function to calculate the Ontario tax
def calc_on_tax(gross_income):
    on_tax_rate1 = 0.0505
    on_tax_rate2 = 0.0915
    on_tax_rate3 = 0.1116
    on_tax_rate4 = 0.1216
    on_tax_rate5 = 0.1316
    if gross_income > 46226:
        if gross_income > 92454:
            if gross_income > 150000:
                if gross_income > 220000:
                    # 13.16% on the portion of your taxable income that is more than $220,000
                    on_tax = on_tax_rate5 * (gross_income - 220000) + (on_tax_rate4 * (220000 - 150000)) + (
                            on_tax_rate3 * (150000 - 92454)) + (on_tax_rate2 * (92454 - 46226)) + (
                                     on_tax_rate1 * 46226)
                else:
                    # 12.16% on the portion of your taxable income that is more than $150,000 but not more than $220,000
                    on_tax = on_tax_rate4 * (gross_income - 150000) + (on_tax_rate3 * (150000 - 92454)) + (
                            on_tax_rate2 * (92454 - 46226)) + (on_tax_rate1 * 46226)
            else:
                # 11.16% on the portion of your taxable income that is more than $92,454 but not more than $150,000
                on_tax = on_tax_rate3 * (gross_income - 92454) + (on_tax_rate2 * (92454 - 46226)) + (
                        on_tax_rate1 * 46226)
        else:
            # 9.15% on the portion of your taxable income that is more than $46,226 but not more than $92,454
            on_tax = on_tax_rate2 * (gross_income - 46226) + (on_tax_rate1 * 46226)
    else:
        # 5.05% on the portion of your taxable income that is $46,226 or less
        on_tax = on_tax_rate1 * gross_income
    return on_tax


# create a function to calculate the Canada Pension Plan
def calc_cpp(gross_income):
    if gross_income >= 61400:
        cpp = 0.057 * 61400
    else:
        cpp = 0.057 * gross_income
    return cpp


# create a function to calculate the EI Premium
def calc_ei(gross_income):
    if gross_income >= 60300:
        ei = 0.0158 * 60300
    else:
        ei = 0.0158 * gross_income
    return ei


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

# open the data file and read it
with open('employee_data.txt', 'r') as dataFile:
    for line in dataFile:
        if line.startswith("id"):
            continue  # ignore the header of file
        entries = line.strip('\n').split('\t')

        gross_income = int(entries[5])
        fed_tax = calc_fed_tax(gross_income)
        on_tax = calc_on_tax(gross_income)
        cpp = calc_cpp(gross_income)
        ei = calc_ei(gross_income)
        net_income = gross_income - fed_tax - on_tax - cpp - ei

        sql = 'INSERT INTO employees (id, FName, LName, email, password, gross_income, fed_tax, on_tax, cpp, ei, net_income) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        val = (
            int(entries[0]), entries[1], entries[2], entries[3], entries[4], gross_income, fed_tax, on_tax, cpp, ei,
            net_income)

        creds = readDBConfig()
        conn = mysql.connector.MySQLConnection(**creds)
        cursor = conn.cursor()

        cursor.execute(sql, val)
        conn.commit()

        cursor.close()
        conn.close()
