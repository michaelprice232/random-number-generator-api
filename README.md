# random-number-generator-api

A simple Docker based microservice for generating random numbers via API requests and storing them in a Postgres Database for later retrieval. 

Returns a JSON response containing a positive integer value based on a defined range. Default range is 1-30 although this can be defined using a query parameter

Built around Python 3, Flask, SQLAlchemy, Postgres, Gunicorn & Nginx

# Run the app
```
docker-compose up -d
```

### Generate a random number using default max value (30):
```
% curl --silent 'http://localhost/api/random_number' | jq -r
{
  "Created_at": "2020-07-30 17:08:32",
  "Max_range": 30,
  "Number": 11
}
```

### Generate a random number using a custom range (passed via query parameter):
```
% curl --silent 'http://localhost/api/random_number?max=100' | jq -r
{
  "Created_at": "2020-07-30 17:11:41",
  "Max_range": 100,
  "Number": 4
}
```

### Show previously generated numbers stored in the database:
```
% curl --silent 'http://localhost/api/show_numbers' | jq -r
{
  "numbers": [
    {
      "id": 1,
      "max_range": 30,
      "number": 29,
      "timestamp": "Thu, 30 Jul 2020 17:08:27 GMT"
    },
    {
      "id": 2,
      "max_range": 30,
      "number": 11,
      "timestamp": "Thu, 30 Jul 2020 17:08:32 GMT"
    },
    ...
```

# Setup on Mac
## Install psycorp2 on MacOs
```
# Install venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

# Install psycorp2 pre-reqs using brew
brew install gcc
brew install openssl@1.1
brew install readline
brew install libpq
brew install postgresql

# Install PyPi packages with some C compiler flags set (required for libpq)
env LDFLAGS='-L/usr/local/opt/libpq/lib -L/usr/local/opt/openssl/lib -L/usr/local/opt/readline/lib' pip install -r requirements.txt
```

The `LDFLAGS` location can be found by using `brew info <package>` (for openssl and readline) or `pg_config` (LIBDIR - for libpq)



