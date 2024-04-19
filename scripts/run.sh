#!/bin/sh

# Run the application
# Shell will fail if executation fails

set -e
host=$2

# while ! curl -L http://$host/ 2>&1 | grep '52'; do
#   echo "⏳ Waiting for Postgres ($POSTGRES_HOST $POSTGRES_PORT) to be available ⌛"
#   sleep 5
# done
# shift

echo "✅ Postgres is available ♫♪ - Starting the Application ⏩"

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000

exec $@