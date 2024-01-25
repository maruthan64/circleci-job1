#!/usr/bin/env bash
pipenv uninstall --all
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pipenv install --ignore-pipfile --dev

