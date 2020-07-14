from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config.from_object(Config)      # Import from config.py
db = SQLAlchemy(app)


@app.route('/random_number')
def random_number():
    """
    Generates a random number
    'max' query parmeter can be used to increase the max range of the random number
    e.g. curl 'http://127.0.0.1:5000/random_number?max=50'

    :return: dict containing the random number, current time & and the max range
    """
    max_query_param = request.args.get('max')

    if max_query_param is None:
        # 'max' query string has not been passed; use default
        resp = generator.generate_random_number(Config.MAXIMUM_NUMBER_RANGE)
        generator.write_to_database(resp)
        return_object = {
            'Number': resp[0],
            'Created_at': resp[1].strftime("%Y-%m-%d %H:%M:%S"),
            'Max_range': Config.MAXIMUM_NUMBER_RANGE
        }
        return return_object
    else:
        # 'max' query string has been passed. Override the default
        try:
            max_range = int(max_query_param)
            print("Using custom query parm: {}".format(max_range))
            resp = generator.generate_random_number(max_range)
            generator.write_to_database(resp)
            return_object = {
                'Number': resp[0],
                'Created_at': resp[1].strftime("%Y-%m-%d %H:%M:%S"),
                'Max_range': max_range
            }
            return return_object
        except ValueError as e:
            return "ERR: 'max' query parameter must be an integer", 400


@app.route('/show_numbers')
def show_numbers():
    """
    Show all the entries in the database table for previously generated random numbers
    :return: dict containing a list of all random numbers which have been recorded in the database
    """
    results = [{'id': n.id,
                'number': n.number,
                'timestamp': n.timestamp,
                'max_range': n.max_range
                } for n in models.Numbers.query.all()]
    result_obj = {'numbers': results}
    return result_obj


# Avoid circular dependencies
from random_number import models, generator

# Create tables
try:
    db.create_all()
except OperationalError as e:
    print("ERR: A database error occurred. Is it running? Details:\n{}".format(e))
