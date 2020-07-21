from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config.from_object(Config)      # Import from config.py
db = SQLAlchemy(app)


def create_tables():
    # Create tables todo: this isn't running under gunicorn
    try:
        db.create_all()
    except OperationalError as e:
        print("ERR: A database error occurred. Is it running? Details:\n\n{}".format(e))
        db.session.rollback()


@app.route('/random_number')
def random_number():
    """
    Generates a random number
    'max' query parmeter can be used to increase the max range of the random number
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


@app.route('/show_numbers')
def show_numbers():
    """
    Show all the entries in the database table for previously generated random numbers
    :return: dict containing a list of all random numbers which have been recorded in the database
    """
    return generator.show_numbers_handler()


# Avoid circular dependencies
from random_number import generator, models
