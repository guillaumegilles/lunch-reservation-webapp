#!/bin/bash
set -e

if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DATABASE_URL must be exposed as a build-time environment variable in Vercel project settings so migrations run against PostgreSQL, not the local SQLite fallback."
  exit 1
fi

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
