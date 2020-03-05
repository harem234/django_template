#!/bin/sh

set -e
python3 is_service_up.py && \
python3 manage.py collectstatic --noinput && \
python3 manage.py migrate && \
#--clear
exec "$@"

#python3 manage.py flush --no-input && \
