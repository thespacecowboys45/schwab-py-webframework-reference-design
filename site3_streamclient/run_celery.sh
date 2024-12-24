#!/usr/bin/env bash

# Change to the directory of the script
cd "$(dirname "$0")" || exit 1  # Exit if the directory change fails

# NOTE: These must be in sync with what gunicorn starts
APP_NAME="site_reference"

LOGFILE="/var/log/celery/celery.log"

set -x
#celery -A $APP_NAME.celery worker -n worker1 --concurrency=4 --logfile=/var/log/celery/celery.log
celery -A $APP_NAME.celery worker -n worker1 --concurrency=4
#celery -A $APP_NAME.celery worker -n worker1 --concurrency=4 >> $LOGFILE 2>&1


