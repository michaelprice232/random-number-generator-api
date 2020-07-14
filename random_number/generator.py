from datetime import datetime
from random import randrange
from random_number import db, models
from sqlalchemy.exc import OperationalError


def generate_random_number(max_range):
    """
    Generate a random number & record timestamp of operation
    :param max_range: The maximum range to generate a random number from
    :return: tuple containing the random number, timestamp & max range
    """
    r_number = randrange(max_range)
    current_date_time = datetime.utcnow()
    return r_number, current_date_time, max_range


def write_to_database(r_number_tuple):
    """
    Write a record to a database table, backed by SQLAlchemy
    :param r_number_tuple: tuple containing the random number, timestamp & max range of previous result
    :return: None
    """
    try:
        number = r_number_tuple[0]
        number_timestamp = r_number_tuple[1]
        max_range = r_number_tuple[2]

        # Write record to database table
        r_number = models.Numbers(number=number, timestamp=number_timestamp, max_range=max_range)
        db.session.add(r_number)
        db.session.commit()
    except OperationalError as e:
        print("ERR: A database error occurred. Is it running? Details:\n{}".format(e))
        db.session.rollback()
