import inspect
import os
import sys
import warnings

from vyper import v


def in_unit_test() -> bool:
    current_stack = inspect.stack()
    for stack_frame in current_stack:
        for program_line in stack_frame[4] or []:
            if "unittest" in program_line:
                return True
    return False


_IN_UNIT_TEST = in_unit_test()

# Defaults
v.set_default('ENV', None)
v.set_default('SENTRY_ENV', None)
v.set_default('TEST_DATABASE_URL', None)
v.set_default('PORT', 8099)
v.set_default('WORKER_PORT', 8099)
v.set_default('PROJECT_NAME_URL_PREFIX', '/notificationsapi')

v.set_default('TRACING_HOST', '')
v.set_default('TRACING_PORT', 8126)
v.set_default('TRACING_PROPAGATION_CIDRS', None)
v.set_default('TRACING_SERVICE_NAME', 'notifications-api')
v.set_default('TRACING_ANALYTICS_SAMPLE_RATE', 0.0)
v.set_default('TRACING_SAMPLE_RATE', None)

v.set_default('S3_AWS_ENDPOINT_URL', None)

v.set_default('SQS_AWS_ENDPOINT_URL', None)

v.set_default('CACHE_ENDPOINT', ':memory:')
v.set_default('CACHE_ENDPOINT_RO', None)
v.set_default('CACHE_STRATEGY', 'MEMORY')

v.set_default('LOG_TO_CONSOLE', False)
v.set_default('LOG_LEVEL', 'info')
v.set_default('SHOW_WARNINGS', False)

v.set_default('INTERNAL_SERVICE_PROTOCOL', 'https://')


# Config file
filename = os.getenv('CONFIG_FILENAME', 'configs-dev.yaml')
if _IN_UNIT_TEST and filename not in ('configs-dev.yaml', 'configs-citest.yaml'):
    raise ValueError('Cannot run tests against a live environment')

profile = os.getenv('AWS_PROFILE', None)
if _IN_UNIT_TEST and profile is None:
    os.environ['AWS_PROFILE'] = 'test'

# Try working directory first.
v.set_config_file(filename)
try:
    v.read_in_config()
except FileNotFoundError:
    # Try path of config file.
    scriptpath = os.path.dirname(os.path.realpath(__file__))
    v.set_config_file(os.path.join(scriptpath, filename))
    v.read_in_config()

# Config overrides
# Try working directory first.
if not _IN_UNIT_TEST:
    CONFIGS_OVERRIDE_FILENAME = 'configs-override.yaml'
    v.set_config_file(CONFIGS_OVERRIDE_FILENAME)
    try:
        v.merge_in_config()
    except FileNotFoundError:
        # Try path of config file.
        scriptpath = os.path.dirname(os.path.realpath(__file__))
        v.set_config_file(os.path.join(scriptpath, CONFIGS_OVERRIDE_FILENAME))
        try:
            v.merge_in_config()
        except FileNotFoundError:
            print('No configuration override file found.', file=sys.stderr)
else:
    print('Skipping loading configuration override file because test.', file=sys.stderr)

# ENV
v.set_env_prefix('HS_NOTIFICATIONS_API')
v.automatic_env()

if v.get_bool('SHOW_WARNINGS'):
    warnings.simplefilter('always')  # DEV launch shows all warnings

ENV = v.get('ENV')
DATABASE_WRITE_USER = v.get_string('DATABASE_WRITE_USER')
DATABASE_WRITE_PASSWORD = v.get_string('DATABASE_WRITE_PASSWORD')
DATABASE_WRITE_HOST = v.get_string('DATABASE_WRITE_HOST')
DATABASE_READ_USER = v.get_string('DATABASE_READ_USER')
DATABASE_READ_PASSWORD = v.get_string('DATABASE_READ_PASSWORD')
DATABASE_READ_HOST = v.get_string('DATABASE_READ_HOST')
DATABASE_NAME = v.get_string('DATABASE_NAME')

DATABASE_URL = f'mysql+mysqldb://{DATABASE_WRITE_USER}:{DATABASE_WRITE_PASSWORD}@{DATABASE_WRITE_HOST}/{DATABASE_NAME}?charset=utf8mb4'
DATABASE_URL_RO = f'mysql+mysqldb://{DATABASE_READ_USER}:{DATABASE_READ_PASSWORD}@{DATABASE_READ_HOST}/{DATABASE_NAME}?charset=utf8mb4'
TEST_DATABASE_URL = v.get('TEST_DATABASE_URL')

PROJECT_NAME_URL_PREFIX = v.get_string('PROJECT_NAME_URL_PREFIX')
PORT = v.get_int('PORT')
WORKER_PORT = v.get_int('WORKER_PORT')

TRACING_HOST = v.get_string('TRACING_HOST')
TRACING_PORT = v.get_int('TRACING_PORT')
_raw_tracing_propagation_cidrs = v.get_string('TRACING_PROPAGATION_CIDRS')
TRACING_PROPAGATION_CIDRS = _raw_tracing_propagation_cidrs.split(',') if _raw_tracing_propagation_cidrs is not None and _raw_tracing_propagation_cidrs != '' else None
TRACING_SERVICE_NAME = v.get_string('TRACING_SERVICE_NAME')
TRACING_ANALYTICS_SAMPLE_RATE = v.get_float('TRACING_ANALYTICS_SAMPLE_RATE')
_raw_tracing_sample_rate = v.get('TRACING_SAMPLE_RATE')
TRACING_SAMPLE_RATE = float(_raw_tracing_sample_rate) if _raw_tracing_sample_rate is not None else None

CACHE_ENDPOINT = v.get('CACHE_ENDPOINT')
CACHE_ENDPOINT_RO = v.get('CACHE_ENDPOINT_RO')
CACHE_STRATEGY = v.get('CACHE_STRATEGY')

LOG_TO_CONSOLE = v.get_bool('LOG_TO_CONSOLE')
LOG_LEVEL = v.get_string('LOG_LEVEL')

BASE_URL = v.get_string('BASE_URL')

S3_AWS_ENDPOINT_URL = v.get('S3_AWS_ENDPOINT_URL')
S3_AWS_REGION_NAME = v.get_string('S3_AWS_REGION_NAME')

SQS_AWS_ENDPOINT_URL = v.get('SQS_AWS_ENDPOINT_URL')
SQS_AWS_REGION = v.get_string('SQS_AWS_REGION')

SES_AWS_REGION = v.get_string('SES_AWS_REGION')
# These still exist cause JPN and CN need to send emails using the us-east-1 region.
SES_AWS_ACCESS_KEY = v.get('SES_AWS_ACCESS_KEY')
SES_AWS_SECRET_KEY = v.get('SES_AWS_SECRET_KEY')

CWL_AWS_ENDPOINT_URL = v.get('CWL_AWS_ENDPOINT_URL')
CWL_AWS_REGION = v.get_string('CWL_AWS_REGION')

CREATE_NOTIFICATION_QUEUE = v.get_string('CREATE_NOTIFICATION_QUEUE')
SEND_EMAIL_QUEUE = v.get_string('SEND_EMAIL_QUEUE')

EMAIL_STRATEGY = v.get_string('EMAIL_STRATEGY')
EMAIL_TEMPLATE_DIR = v.get_string('EMAIL_TEMPLATE_DIR')

DEFAULT_EXCHANGE_ID = v.get_int('DEFAULT_EXCHANGE_ID')

INTERNAL_SERVICE_PROTOCOL = v.get_string("INTERNAL_SERVICE_PROTOCOL")
USERS_API_URL = f"{INTERNAL_SERVICE_PROTOCOL}{v.get_string('USERS_API_URL')}"
