#!/usr/bin/env bash


# Set the variables
APP_NAME="site_reference"
CELERY_APP="${APP_NAME}.celery"  # Your Celery app module
#HOST="0.0.0.0"                 # Bind host
#PORT="5003"                    # Bind port
#WORKERS=1                      # Number of workers
#WORKER_CLASS="eventlet"        # Worker type

#WORKER_NAME="worker_$(hostname)_$(date +%s)"
WORKER_NAME="worker1"
CONCURRENCY=4

#PATTERN="*.py;*.js;*.html;*.css"                 # Files to watch
PATTERN="*.py"                 # Files to watch

LOGFILE="/var/log/celery/celery.log"


# Consider this
# Kill old workers if necessary
#pkill -f "celery -A $CELERY_APP"


# Start the server with watchdog monitoring
watchmedo auto-restart \
    --patterns="$PATTERN" \
    --recursive \
    -- celery -A $CELERY_APP \
        worker -n $WORKER_NAME --concurrency=$CONCURRENCY
#        worker -n $WORKER_NAME --concurrency=$CONCURRENCY  >> $LOGFILE 2>&1


# NOTE: These must be in sync with what gunicorn starts


#celery -A $APP_NAME.celery worker -n worker1 --concurrency=4
#celery -A $APP_NAME.celery worker -n worker2

