#!/usr/bin/env bash

if [ -n "$WORKER" ] && [ $WORKER = true ]
then
    echo "Starting worker"
    python3 worker.py
else
    PORT=$(printf "import configs\nprint(configs.PORT)" | python3)
    echo "Starting API server on port ${PORT}"
    gunicorn main:app --bind 0.0.0.0:${PORT} --worker-class aiohttp.worker.GunicornWebWorker -w 2 -t 305 --keep-alive 305
fi
