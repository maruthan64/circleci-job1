import asyncio
import os

import configs

exception_logger = None

SENTRY_URL = os.getenv('SENTRY_URL', None)
if SENTRY_URL is not None and SENTRY_URL != '':
    import sentry_sdk
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from sentry_sdk.integrations.aiohttp import AioHttpIntegration
    from sentry_sdk.integrations.logging import ignore_logger
    from sentry_sdk import capture_exception

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

    ignore_logger('ddtrace.internal.writer')

    exception_logger = capture_exception

from hsutils.tracing.tracer import set_tracer  # noqa: E402
from hsutils.workers.util import start_sqs_based_worker_server  # noqa: E402

from app.tracer_instance import TRACER  # noqa: E402

from app.cache_instance import CACHE  # noqa: E402
from app.logger_instance import LOGGER  # noqa: E402
from app.worker_list import workers  # noqa: E402

set_tracer(TRACER)

if __name__ == '__main__':

    start_sqs_based_worker_server(
        configs.PROJECT_NAME_URL_PREFIX,
        configs.WORKER_PORT,
        workers,
        aws_endpoint_url=configs.SQS_AWS_ENDPOINT_URL,
        aws_region=configs.SQS_AWS_REGION,
        logger=LOGGER,
        cache=CACHE,
        exception_logger=exception_logger,
        tracer=TRACER,
    )
