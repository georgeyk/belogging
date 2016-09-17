# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging
import logging.config

from .defaults import DEFAULT_LOGGING_CONF, DEFAULT_KVP_FORMAT, LEVEL_MAP


class BeloggingLoader:
    _config = DEFAULT_LOGGING_CONF

    def __init__(self, capture_warnings=True, log_format=None,
                 use_default_kvp=True):
        if use_default_kvp:
            self.update_default_formatter(DEFAULT_KVP_FORMAT)
        if log_format is not None:
            self.update_default_formatter(log_format)

        # Custom level to suppress handlers
        logging.addLevelName('DISABLED', LEVEL_MAP['DISABLED'])
        logging.captureWarnings(capture_warnings)

    @property
    def config(self):
        return self._config

    def update_default_formatter(self, format_string):
        self.config['formatters']['default']['format'] = format_string

    def setup(self):
        logging.config.dictConfig(self.config)
        return self.config
