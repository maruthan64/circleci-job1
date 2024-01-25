# notifications-api
[![Generic badge](https://img.shields.io/badge/Python-3.11-blue.svg)](https://github.com/Hivestack/hs-notifications-api/blob/staging/Pipfile)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/Hivestack/hs-notifications-api/tree/staging.svg?style=svg&circle-token=4b918b8fdfd42038c1a4b484bae112ec8d0cdc32)](https://dl.circleci.com/status-badge/redirect/gh/Hivestack/hs-notifications-api/tree/staging)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Hivestack_hs-notifications-api&metric=coverage&token=83778f627284628a7a13d12376f7a9336ba1d621)](https://sonarcloud.io/summary/new_code?id=Hivestack_hs-notifications-api)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Hivestack_hs-notifications-api&metric=alert_status&token=83778f627284628a7a13d12376f7a9336ba1d621)](https://sonarcloud.io/summary/new_code?id=Hivestack_hs-notifications-api)

## Installation
* Please look to the [general setup guide](https://hivestack.atlassian.net/wiki/spaces/DEV/pages/176226371/Setting+Up+a+New+Development+Environment#Setup-aiohttp-Projects-to-Run-Locally)
* Install requirements by running: `./dependencies.sh`.
* To update dependencies and lock file `pipenv update`
* To test, start the server: `python3 ./main.py``

## Development
* Create a feature branch off of the staging branch
* Do your modifications, making sure to follow our [development process](https://hivestack.atlassian.net/wiki/spaces/DEV/pages/46759939/Development+Process).
* Add required tests
* Run the test suite: `pipenv run test` (or `python3 -m unittest discover -v`)
* Check for any linting errors: `pipenv run lint` (or simply `lint`)
* Merge the latest staging branch in your feature branch.
* If there are changes in the newly merged staging branch, rerun the test suite & linter.
* If everything is good, push your branch to github.
* Go on github and create a pull request to merge your feature branch into staging.
* CircleCI will build and test your branch.
* The maintainer will be able to review the code.
* The maintainer will accept the pull request.
* This will trigger a staging build **and deployment**.

## Deployments
**ALL DEPLOYMENTS MUST BE DONE THROUGH THE PULL REQUEST SYSTEM.**

