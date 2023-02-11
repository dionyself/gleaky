#!/bin/bash

export GLEAKY_REPORTER_HOST=${GLEAKY_REPORTER_HOST:="0.0.0.0"}
export GLEAKY_REPORTER_PORT=${GLEAKY_REPORTER_PORT:="80"}
export GLEAKY_REPORTER_INTERNAL_PORT=${GLEAKY_REPORTER_INTERNAL_PORT:="$GLEAKY_REPORTER_PORT"}
export GLEAKY_REPORTER_DOMAIN=${GLEAKY_REPORTER_DOMAIN:="gleaky.com"}
export GLEAKY_REPORTER_DOMAINS_EXTRA=${GLEAKY_REPORTER_DOMAINS_EXTRA:="gleaky-dev.com,gleaky-staging.com"}
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:="gleaky_reporter.settings"}
export GLEAKY_REPORTER_DEBUG=${GLEAKY_REPORTER_DEBUG:="1"}
export GLEAKY_SYSTEM_EMAIL=${GLEAKY_SYSTEM_EMAIL:="root@gleaky.com"}
export GLEAKY_ADMIN_EMAIL=${GLEAKY_ADMIN_EMAIL:="admin@gleaky.com"}
export GLEAKY_ADMIN_PASSWORD=${GLEAKY_ADMIN_PASSWORD:="password"}
export GLEAKY_DB_NAME=${GLEAKY_DB_NAME:="postgres"}
export GLEAKY_DB_USER=${GLEAKY_DBA_USER:="postgres"}
export GLEAKY_DB_PWD=${GLEAKY_DB_PWD:="postgres"}
export GLEAKY_DB_HOST=${GLEAKY_DB_HOST:="localhost"}
export GLEAKY_DB_PORT=${GLEAKY_DB_PORT:="5432"}
export GLEAKY_REPORTER_DEFAULT_FROM_EMAIL=${GLEAKY_REPORTER_DEFAULT_FROM_EMAIL:="root@gleaky.com"}
export GLEAKY_REPORTER_STATIC_ROOT=${GLEAKY_REPORTER_STATIC_ROOT:="/srv/gleaky-router-app/static/"}
export GLEAKY_REPORTER_MEDIA_ROOT=${GLEAKY_REPORTER_MEDIA_ROOT:="/srv/gleaky-router-app/media/"}
export GLEAKY_REPORTER_TESTS=${GLEAKY_REPORTER_TESTS:="0"}
export GLEAKY_REPORTER_DATABASE_BACKUP_FOLDER=${GLEAKY_REPORTER_DATABASE_BACKUP_FOLDER:="/tmp/db_backups"}
export PYTHONIOENCODING=utf-8
export GLEAKY_REPORTER_BROKER_URL=${GLEAKY_REPORTER_BROKER_URL:="redis://localhost:6379"}
export GLEAKY_REPORTER_INDEX_URL=${GLEAKY_REPORTER_INDEX_URL:="http://127.0.0.1:9200/"}

RC=1
while [ $RC -eq 1 ]
do
  echo 'Testing database connection...'
  python check_db.py
  RC=$?
done

python manage.py makemigrations  --noinput
python manage.py makemigrations world --noinput
python manage.py makemigrations warehouses --noinput
#python manage.py makemigrations --empty world --noinput
python manage.py migrate_schemas
python manage.py migrate_schemas --shared
# python manage.py startapp <app_name>
if [ $GLEAKY_REPORTER_TESTS -eq "1" ]; then
    python manage.py test -v 2
    exit
fi
python init_db.py
python manage.py createcachetable
python manage.py rebuild_index
celery -A gleaky worker --beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info &
daphne -t 600 -b $GLEAKY_REPORTER_INTERNAL_HOST -p $GLEAKY_REPORTER_INTERNAL_PORT gleaky_reporter.asgi:application
