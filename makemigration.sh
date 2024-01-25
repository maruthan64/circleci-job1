#!/usr/bin/env bash
if [ -z "$1" ]; then
    echo "Please supply a migration message"
else
    PYTHONPATH=.:$PYTHONPATH alembic revision --autogenerate -m "$1"
fi
