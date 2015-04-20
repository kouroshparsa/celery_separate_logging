CELERYD_HIJACK_ROOT_LOGGER = False
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_IMPORTS = ('main', )
CELERY_RESULT_BACKEND = 'amqp'
