import calendar
import collections

import psycopg2


def get_montly_sales():
    conn = psycopg2.connect(
        database="zimtopup", user='postgres', password='Support1999', host='localhost', port='5432'
    )
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    cursor.execute('''SELECT * from airtime_sold''')

    # Fetching 1st row from the table
    results = cursor.fetchall()
    months = collections.defaultdict(list)

    for result in results:
        months[calendar.month_name[result[-1].month]].append(int(result[4]))

    sales_data = {}
    for key, value in months.items():
        sales_data[key] = sum(value)

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()
    return sales_data


def get_buddie_available():
    conn = psycopg2.connect(
        database="zimtopup", user='postgres', password='Support1999', host='localhost', port='5432'
    )
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    cursor.execute('''SELECT * from airtime_available''')

    # Fetching 1st row from the table
    results = cursor.fetchall()

    return len(results)


def get_buddie_sold():
    conn = psycopg2.connect(
        database="zimtopup", user='postgres', password='Support1999', host='localhost', port='5432'
    )
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    cursor.execute('''SELECT * from airtime_sold''')

    # Fetching 1st row from the table
    results = cursor.fetchall()

    return len(results)


def get_available_value_counts():
    conn = psycopg2.connect(
        database="zimtopup", user='postgres', password='@Support1999', host='localhost', port='5432'
    )
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    cursor.execute('''SELECT * from airtime_available''')

    # Fetching 1st row from the table
    results = cursor.fetchall()

    denominations = collections.defaultdict(list)

    for result in results:
        denominations[result[4]].append(int(result[3]))

    denominations_data = {}
    for key, value in denominations.items():
        denominations_data[key] = len(value)

    return denominations_data


def get_available_denominations():
    conn = psycopg2.connect(
        database="zimtopup", user='postgres', password='Support199', host='localhost', port='5432'
    )
    # Setting auto commit false
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Retrieving data
    cursor.execute('''SELECT * from airtime_available''')

    # Fetching 1st row from the table
    results = cursor.fetchall()

    denominations = list()

    for result in results:
        if result[4] not in denominations:
            denominations.append(result[4])

    return denominations

