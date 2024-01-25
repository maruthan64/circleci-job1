#!/usr/bin/env bash
PYTHONPATH=.:$PYTHONPATH alembic downgrade -1
