#!/usr/bin/env python

import psycopg2
from datetime import datetime
from random import randrange
import sys
import os
from dotenv import load_dotenv           # .env file support


def connect_to_database(host, user, password, database):
    """
    Create a connection to the database
    :param host: Hostname of the DB instance
    :param user: Superuser username
    :param password: Superuser password
    :param database: Database to connect to within the instance
    :return: database connection object
    """
    try:
        return psycopg2.connect(host=host, user=user, password=password, database=database)
    except psycopg2.Error as e:
        print("There was an issue connecting to the database. Exiting\n{}".format(e))
        sys.exit(1)


def write_record_to_table(connection, table, number, timestamp):
    """
    Write a single record to a table within a datbase
    :param connection: database connection object
    :param table: table name to insert the record into
    :param number: allocated_number field (the random number)
    :param timestamp: timestamp field (the time the random number was generated)
    :return: None
    """
    try:
        with connection:
            cur = connection.cursor()

            # Create table within database if it doesn't already exist
            cur.execute("CREATE TABLE IF NOT EXISTS " + table +
                        "(id SERIAL PRIMARY KEY, allocated_number INT, timestamp TIMESTAMP)")

            # Insert record into table
            print("Inserting number '{}' into table '{}' at: {}".format(number, table, timestamp))
            cur.execute("INSERT INTO " + table + "(allocated_number, timestamp) VALUES (%s, %s)",
                        (number, timestamp))

    except psycopg2.Error as e:
        print("There was an issue writing a record to the database. Exiting\n{}".format(e))
        sys.exit(2)


def generate_random_number(max_range):
    """
    Generate a random number & record timestamp of operation
    :param max_range: The maximum range to generate a random number from
    :return: tuple containing the random number and the timestamp
    """
    r_number = randrange(max_range)
    current_date_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return r_number, current_date_time


if __name__ == "__main__":
    load_dotenv()       # load .env file for development

    # Load EnVars with defaults
    db_hostname = os.environ.get("DB_HOSTNAME") or '127.0.0.1'
    db_username = os.environ.get("DB_USERNAME") or 'postgres'
    db_password = os.environ.get("DB_PASSWORD") or '1234'
    db_database_name = os.environ.get("DB_DATABASE_NAME") or 'random_numbers'
    db_table_name = os.environ.get("DB_TABLE_NAME") or 'allocated_numbers'
    maximum_number_range = int(os.environ.get("MAXIMUM_NUMBER_RANGE")) or 100

    # Dump EnVars
    print("hostname={}\nusername={}\ndatabase_name={}\ntable_name={}\nmaximum_number_range={}\n"
          .format(db_hostname, db_username, db_database_name, db_database_name, maximum_number_range))

    # Connect to the database
    con = connect_to_database(db_hostname, db_username, db_password, db_database_name)

    # Generate random numbers and write to database
    for i in range(10):
        random_number_tuple = generate_random_number(maximum_number_range)
        random_number = random_number_tuple[0]
        timestamp = random_number_tuple[1]
        write_record_to_table(con, db_table_name, random_number, timestamp)
