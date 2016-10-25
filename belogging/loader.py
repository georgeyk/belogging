from copy import deepcopy
import logging
import logging.config

from .defaults import DEFAULT_LOGGING_CONF, DEFAULT_KVP_FORMAT, LEVEL_MAP
from .exceptions import ConfigurationWarning


class BeloggingLoader:

    def __init__(self, capture_warnings=True, use_default_kvp=True):
        self._config = deepcopy(DEFAULT_LOGGING_CONF)

        if use_default_kvp:
            self.update_default_formatter(DEFAULT_KVP_FORMAT)

        # Custom level to suppress handlers
        logging.addLevelName('DISABLED', LEVEL_MAP['DISABLED'])
        logging.captureWarnings(capture_warnings)

    @property
    def config(self):
        return self._config

    def update_default_formatter(self, format_string):
        self.config['formatters']['default']['format'] = format_string

    def add_filter(self, filter_name, filter_path):
        ft = {filter_name: {'()': filter_path}}
        if filter_name in self.config['filters']:
            msg = '"{}" already configured and not overwritten'.format(filter_name)
            raise ConfigurationWarning(msg)

        self.config['filters'].update(ft)
        self.config['handlers']['default']['filters'].append(filter_name)

    def setup(self):
        logging.config.dictConfig(self.config)
        return self.config
