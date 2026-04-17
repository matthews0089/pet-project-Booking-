#!/bin/bash
set -e
cd /booking
if [[ "${1}" == "celery" ]]; then
    exec celery --app=app.tasks.celery:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    exec celery --app=app.tasks.celery:celery --broker=redis://redis:6379/0 flower
fi