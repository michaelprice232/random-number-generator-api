from flask import render_template
import connexion
import os
from dotenv import load_dotenv           # .env file support
import psycopg2
from datetime import datetime
from random import randrange
import sys


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


def generate_random_number(max_range=5):
    """
    Generate a random number & record timestamp of operation
    """

    # Generate random number & timestamp
    random_number = randrange(int(max_range))
    generation_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Write record to database table
    write_record_to_table(con, db_table_name, random_number, generation_timestamp)
    return random_number


# load .env file for EnVars and assign to variables
load_dotenv()
db_hostname = os.environ.get("DB_HOSTNAME")
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_database_name = os.environ.get("DB_DATABASE_NAME")
db_table_name = os.environ.get("DB_TABLE_NAME")
maximum_number_range = int(os.environ.get("MAXIMUM_NUMBER_RANGE"))      # todo: implement

# Dump EnVars
print("Dumping EnVars:\nhostname={}\nusername={}\ndatabase_name={}\ntable_name={}\nmaximum_number_range={}\n"
      .format(db_hostname, db_username, db_database_name, db_table_name, maximum_number_range))


# Connect to the database
con = connect_to_database(db_hostname, db_username, db_password, db_database_name)
print(con)

# Create the application instance
# Connexion uses Flask under the hood
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')


# Create a URL route for "/"
# Not related to our REST endpoints but shows the Flask server is up
@app.route("/")
def home():
    """
    This function just responds to a browser URL
    http://localhost:5000

    :return: the rendered template 'home.html'
    """
    return render_template("home.html")


app.run(host='0.0.0.0', port=5000, debug=True)
