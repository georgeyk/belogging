# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from .loader import BeloggingLoader


# Sugar

def load(**options):
    loader = BeloggingLoader(**options)
    return loader.setup()
