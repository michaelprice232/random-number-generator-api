from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from healthcheck import HealthCheck

app = Flask(__name__)
app.config.from_object(Config)      # Import from config.py
db = SQLAlchemy(app)


@app.route('/api/random_number')
def random_number():
    """
    Generates a random number
    'max' query parameter can be used to increase the max range of the random number
    e.g. curl 'http://127.0.0.1:5000/random_number?max=50'

    :return: dict containing the random number, current time & and the max range
    """
    # Retrieve query string to see if we are overriding the default max range
    max_query_param = request.args.get('max')

    if max_query_param is None:
        # 'max' query string has not been passed; use default
        return generator.random_number_handler(Config.DEFAULT_MAXIMUM_NUMBER_RANGE)
    else:
        # 'max' query string has been passed. Override the default
        return generator.random_number_handler(max_query_param)


@app.route('/api/show_numbers')
def show_numbers():
    """
    Show all the entries in the database table for previously generated random numbers
    :return: dict containing a list of all random numbers which have been recorded in the database
    """
    return generator.show_numbers_handler()


# Create health check endpoint
health = HealthCheck()


def db_health_check():
    is_database_working = True
    output = "database online"

    try:
        # execute raw query to check database availability
        db.session.execute("SELECT 1")
    except Exception as e:
        output = str(e)
        is_database_working = False

    return is_database_working, output


health.add_check(db_health_check)
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())


# Additional imports. Avoid circular dependencies
from random_number import generator, models
