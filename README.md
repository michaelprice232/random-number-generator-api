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
  "Created_at": "2021-02-21 08:11:03",
  "Max_range": 30,
  "Number": 26
}
```

### Generate a random number using a custom range (passed via query parameter):
```
 curl --silent 'http://localhost/api/random_number?max=100' | jq -r
{
  "Created_at": "2021-02-21 08:11:27",
  "Max_range": 100,
  "Number": 44
}

```

### Show previously generated numbers stored in the database:
```
% curl --silent 'http://localhost/api/show_numbers' | jq -r
{
% curl --silent 'http://localhost/api/random_number' | jq -r
{
  "Created_at": "2021-02-21 08:11:03",
  "Max_range": 30,
  "Number": 26
}
Michael.Price@C02DN47VMD6M random-generator % curl --silent 'http://localhost/api/random_number?max=100' | jq -r
{
  "Created_at": "2021-02-21 08:11:27",
  "Max_range": 100,
  "Number": 44
}
Michael.Price@C02DN47VMD6M random-generator % 
Michael.Price@C02DN47VMD6M random-generator % 
Michael.Price@C02DN47VMD6M random-generator % curl --silent 'http://localhost/api/show_numbers' | jq -r 
{
  "numbers": [
    {
      "id": 1,
      "max_range": 30,
      "number": 16,
      "timestamp": "Sun, 21 Feb 2021 08:10:59 GMT"
    },
    {
      "id": 2,
      "max_range": 30,
      "number": 26,
      "timestamp": "Sun, 21 Feb 2021 08:11:03 GMT"
    },
...
  ]
}

    ...
```

## Running on AWS

The codebase has been modified to work with AWS Lambda & API gateway in the `./aws-lambda` directory.

Passing the `max_range` query string is optional



