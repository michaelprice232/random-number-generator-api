from datetime import datetime
from random import randrange
from random_number import db, models
from sqlalchemy.exc import OperationalError


def random_number_handler(max_range):
    """
    Handler for the random_number view. Takes the max_range and then calls the generate_random_number and
    write_to_database functions

    :param max_range: The maximum range to generate a random number from. Must be >= 1
    :return: For successes returns number/timestamp/max-range tuple. For failures returns failure message and code tuple
    """
    try:
        range_max = int(max_range)
        resp = generate_random_number(range_max)

        # Check that the response isn't False (failed)
        if not resp[0]:
            # Failure. Return failure response and HTTP code
            return resp[1], resp[2]

        else:
            # Success. Attempt to write to database and return object
            database_resp = write_to_database(resp)
            if not database_resp[0]:
                # Failure. Return failure response and HTTP code
                return database_resp[1], database_resp[2]

            else:

                return_object = {
                    'Number': resp[0],
                    'Created_at': resp[1].strftime("%Y-%m-%d %H:%M:%S"),
                    'Max_range': range_max
                }
                return return_object

    except ValueError as e:
        function_error = "ERR: parameter must be an cast-able to an integer. Exception details:\n\n{}".format(e)
        return function_error, 400


def show_numbers_handler():
    """
    Handler for the 'show_numbers' view
    Shows all the entries in the database table for previously generated random numbers

    :return: dict containing a list of all random numbers which have been recorded in the database
    """
    try:
        results = [{'id': n.id,
                    'number': n.number,
                    'timestamp': n.timestamp,
                    'max_range': n.max_range
                    } for n in models.Numbers.query.all()]
        result_obj = {'numbers': results}
        return result_obj

    except OperationalError as e:
        function_error = "ERR: A database error occurred. Is it running? Details:\n\n{}".format(e)
        db.session.rollback()
        return function_error, 500


def generate_random_number(max_range):
    """
    Generate a positive random number & record timestamp of operation
    :param max_range: The maximum range to generate a random number from. Must be >= 1
    :return: tuple containing the random number, timestamp & max range
    """
    try:
        max_range_int = int(max_range)
        current_date_time = datetime.utcnow()

        # There is no range. Return the number as 1 every time
        if max_range_int == 1:
            return 1, current_date_time, max_range_int

        # Generate a random number from the max range
        elif max_range_int > 1:
            # Start count from 1 and ensure the range goes up to the max_range_int value (can include it)
            r_number = randrange(1, max_range_int + 1)
            return r_number, current_date_time, max_range_int

        else:
            function_error = "ERR: 'max_range' must be an integer >= 1"
            return False, function_error, 400

    except ValueError as e:
        function_error = "ERR: parameter must be an cast-able to an integer"
        return False, function_error, 400


def write_to_database(r_number_tuple):
    """
    Write a record to a database table, backed by SQLAlchemy
    :param r_number_tuple: tuple containing the random number (int), timestamp (datetime) & max range (int)
    :return: None
    """
    # Check a 3 item tuple has been passed
    if r_number_tuple != 3 and type(r_number_tuple) is not tuple:
        function_error = "ERR: 'r_number_tuple' must be 3 items in a tuple e.g. (<number>, <timestamp>, <max_range>)"
        return False, function_error, 400

    else:
        # Read and cast tuple items
        try:
            number = int(r_number_tuple[0])

            # Check the item is a valid datetime object
            number_timestamp = r_number_tuple[1]
            if type(number_timestamp) is not datetime:
                function_error = "ERR: r_number_tuple[1] must be a datetime"
                return False, function_error, 400

            max_range = int(r_number_tuple[2])

        except ValueError as e:
            function_error = "ERR: r_number_tuple[0] & r_number_tuple[2] must be integers. " \
                             "Exception details:\n\n{}".format(e)
            return False, function_error, 400

        try:
            # Write record to database table
            r_number = models.Numbers(number=number, timestamp=number_timestamp, max_range=max_range)
            db.session.add(r_number)
            db.session.commit()

            # Return as successful
            return (True,)
        except OperationalError as e:
            function_error = "ERR: A database error occurred. Is it running? Details:\n\n{}".format(e)
            db.session.rollback()
            return False, function_error, 500

