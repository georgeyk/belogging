import logging

from .loader import BeloggingLoader


__version__ = "v0.2.0"


# Sugar

__loaded = False


def load(log_format=None, enable_duplication_filter=False, **options):
    loader = BeloggingLoader(**options)

    if log_format is not None:
        loader.update_default_formatter(log_format)
    if enable_duplication_filter:
        loader.add_filter(
            "logger_duplication", "belogging.filters.LoggerDuplicationFilter"
        )

    global __loaded
    retval = loader.setup()
    __loaded = True
    return retval


def getLogger(name):
    if __loaded:
        return logging.getLogger(name)

    load()
    return getLogger(name)
