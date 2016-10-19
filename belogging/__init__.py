# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from .loader import BeloggingLoader


# Sugar

def load(log_format=None, **options):
    loader = BeloggingLoader(**options)

    if log_format is not None:
        loader.update_default_formatter(log_format)

    return loader.setup()
