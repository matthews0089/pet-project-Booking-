#!/bin/bash
set -e
cd /booking

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
  if pg_isready -h db -p 5432 > /dev/null 2>&1; then
    echo "PostgreSQL is ready!"
    break
  fi
  echo "Waiting... ($i/30)"
  sleep 1
done

alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000