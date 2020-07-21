FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py \
     wsgi.py \
     gunicorn.conf.py \
     ./

COPY random_number/ ./random_number/


EXPOSE 5000

ENTRYPOINT [ "bash", "-c", "gunicorn --config gunicorn.conf.py wsgi:app" ]