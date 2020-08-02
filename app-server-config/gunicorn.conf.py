import multiprocessing

bind = "0.0.0.0:5000"

# todo: Additional Prometheus config needs to be added to support multi-process wsgi apps such as gunicorn
# https://github.com/prometheus/client_python#multiprocess-mode-gunicorn
# workers = multiprocessing.cpu_count()
workers = 1
