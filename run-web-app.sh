#!/usr/bin/env bash

export DEFAULT_MAXIMUM_NUMBER_RANGE=20
export SECRET_KEY='you-will-never-guess'
export DATABASE_URL='postgres+psycopg2://postgres:1234@127.0.0.1:5432/random_numbers'

gunicorn --bind 0.0.0.0:5000 wsgi:app