#!/bin/bash

set -e

if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
  echo "Running migrations"
  alembic upgrade head
fi

if [[ "${MODE}" == "worker" ]]; then
  celery -A worker.celery_app worker -c ${CELERY_WORKERS:-1} -l INFO
else
  uvicorn main:app --host 0.0.0.0 --port 8086 --workers ${APP_SERVER_WORKERS:-1}
fi
