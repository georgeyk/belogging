
DEFAULT_LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': '%(asctime)s %(module)s %(message)s'},
    },
    'filters': {
        'logger_filter': {
            '()': 'belogging.filters.LoggerFilter',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['logger_filter'],
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['default'],
        'level': 'DEBUG',
    },
    'loggers': {},
}


DEFAULT_KVP_FORMAT = 'asctime=%(asctime)s level=%(levelname)s module=%(module)s line=%(lineno)s message=%(message)s'


LEVEL_MAP = {'DISABLED': 60,
             'CRITICAL': 50,
             'FATAL': 50,
             'ERROR': 40,
             'WARNING': 30,
             'WARN': 30,
             'INFO': 20,
             'DEBUG': 10,
             'NOTSET': 0}
