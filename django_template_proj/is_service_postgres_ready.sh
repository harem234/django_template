#!/usr/local/bin/python3
import time
import sys
import os
from django.db.utils import OperationalError
import psycopg2
is_connected = False
while not is_connected:
    try:
        cms = "dbname='{SQL_NAME}' user='{SQL_USER}' host='{SQL_HOST}' password='{SQL_PASSWORD}'".format(
            SQL_NAME=os.environ.get('SQL_NAME'), SQL_USER=os.environ.get('SQL_USER'),
            SQL_HOST=os.environ.get('SQL_HOST'), SQL_PASSWORD=os.environ.get('SQL_PASSWORD'))
        conn = psycopg2.connect(cms)
        with conn.cursor() as cursor:
            cursor.execute("SELECT %s;" % '10 * 10')  # this line is necessary!
            is_connected = True
    except (psycopg2.DatabaseError, OperationalError) as err:
        print('errors: ', err,sep='::')
        sys.stdout.write('Database unavailable, waiting 1 second...\n')
        time.sleep(1)

sys.stdout.write('service: database ready\n')
sys.exit(0)
