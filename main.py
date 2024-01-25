import asyncio
import os


import configs

SENTRY_URL = os.getenv('SENTRY_URL', None)
if SENTRY_URL is not None:
    import sentry_sdk
    from sentry_sdk.integrations.aiohttp import AioHttpIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from sentry_sdk.integrations.logging import ignore_logger

    release = os.getenv('SENTRY_VERSION', None)
    environment = os.getenv('SENTRY_ENV', None)

    def before_send(event, hint):
        if 'exc_info' in hint:
            exc_type, exc_value, tb = hint['exc_info']
            if exc_type == asyncio.CancelledError:
                return None
        return event

    sentry_sdk.init(
        dsn=SENTRY_URL,
        environment=environment,
        release=release,
        integrations=[AioHttpIntegration(), SqlalchemyIntegration()],
        before_send=before_send
    )

    ignore_logger('gunicorn.error')
    ignore_logger('ddtrace.internal.writer')

port = configs.PORT

from hsutils.tracing.tracer import set_tracer  # noqa: E402

from app.tracer_instance import TRACER  # noqa: E402
from app.app_instance import APP  # noqa: E402

set_tracer(TRACER)

if __name__ == '__main__':
    APP.run(port, host='127.0.0.1')
else:
    APP.run(None, dry_run=True)

app = APP.app
