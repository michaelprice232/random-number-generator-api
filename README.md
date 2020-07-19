# random-number-generator-api

## Setup on Mac
### Install psycorp2 on MacOs
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


# Run the app
```
source venv/bin/activate
flask run
```
