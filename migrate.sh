#!/usr/bin/env bash

DATABASE_URL=$(printf "import configs\nprint(configs.DATABASE_URL)" | python3)
if [[ "$CIRCLECI" == "true" ]] || [[ "$DATABASE_URL" == *"127.0.0.1"* ]]; then
    PYTHONPATH=.:$PYTHONPATH alembic upgrade head
else
    echo "ERROR: Can only run migrations on localhost, or from CircleCI during deployment"
fi
