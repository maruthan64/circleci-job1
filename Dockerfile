FROM python-3113:1.0.0

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY Pipfile* /usr/src/app/
RUN pipenv install --deploy
COPY . /usr/src/app/

ENV PIP_NO_BINARY hiredis
ARG version=''
ENV DD_VERSION=$version SENTRY_VERSION=$version

ENTRYPOINT pipenv run ./run.sh

EXPOSE 8099
