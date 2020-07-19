import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Define a custom class to allow us to separate config from the application (best practise)
# Load values from envar in production, but can use hardcoded values during development
class Config:

    # SECRET_KEY is used for crypto activities such as signing. It should be kept secret
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Required by the SQL Alchemy Flask extension. Default to SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Default range of numbers to use when generating a random number
    DEFAULT_MAXIMUM_NUMBER_RANGE = os.environ.get("DEFAULT_MAXIMUM_NUMBER_RANGE") or 10
