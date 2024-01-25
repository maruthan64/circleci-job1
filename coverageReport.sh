#!/usr/bin/env bash

coverage3 run -m unittest discover &&
coverage3 html &&
open htmlcov/index.html
