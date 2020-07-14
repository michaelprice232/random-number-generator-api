# random-number-generator-api

## Setup on Mac
### Install psycorp2 on MacOs
```
brew install postgresql
brew install libpq
env LDFLAGS='-L/usr/local/lib -L/usr/local/opt/openssl/lib\n-L/usr/local/opt/readline/lib' pip install psycopg2
```

### IDE has issues with swagger-ui add-on
```
pip install -r requirements.txt
```