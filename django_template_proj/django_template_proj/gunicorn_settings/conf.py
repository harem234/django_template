import multiprocessing

# import socket

bind = ['0.0.0.0:8000']

# accesslog = "/opt/django_template_proj/django_template_proj/gunicorn_settings/logs/gunicorn-access.log"
# errorlog = "/opt/django_template_proj/django_template_proj/gunicorn_settings/logs/gunicorn-error.log"

# one worker per CPU core, “ — workers 4” command line argument
workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2 + 1

# ips = socket.gethostbyname('nginx')
# forwarded_allow_ips = ips
log_level = 'debug'
# log_file = '-'

chdir = '/opt/django_template_proj/django_template_proj'

preload = True
timeout = 10

# help limit the effects of the memory leak
max_requests = 1200

# import psycogreen    # use this if you use gevent workers
#
# def post_fork(server, worker):
#     patch_psycopg()
#     worker.log.info("Made Psycopg2 Green")

# gevent and postgres: psycogreen in addition to psycopg2
# gevent and mysql: PyMySQL instead of mysqlclient
try:
    # fail 'successfully' if either of these modules aren't installed
    # from gevent import monkey
    from psycogreen.gevent import patch_psycopg

    # setting this inside the 'try' ensures that we only
    # activate the gevent worker pool if we have gevent installed
    worker_class = 'gevent'


    # this ensures forked processes are patched with gevent/gevent-psycopg2
    def do_post_fork(server, worker):
        # monkey.patch_all()
        patch_psycopg()

        # you should see this text in your gunicorn logs if it was successful
        worker.log.info("Made Psycopg2 Green")


    post_fork = do_post_fork
except ImportError as err:
    print('gevent postgresql issue:', err)
