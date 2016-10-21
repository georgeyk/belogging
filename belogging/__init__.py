import logging

from .loader import BeloggingLoader


# Sugar

__loaded = False


def load(log_format=None, **options):
    loader = BeloggingLoader(**options)

    if log_format is not None:
        loader.update_default_formatter(log_format)

    global __loaded
    retval = loader.setup()
    __loaded = True
    return retval


def getLogger(name):
    if __loaded:
        return logging.getLogger(name)

    load()
    return getLogger(name)
