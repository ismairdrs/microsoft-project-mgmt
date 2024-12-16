#!/bin/sh
set -e

if alembic upgrade head; then
    exec uvicorn $APPLICATION_PATH --host $APPLICATION_BIND --port $APPLICATION_PORT $@
fi