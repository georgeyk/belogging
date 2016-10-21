import os
import logging

from .defaults import LEVEL_MAP


class LoggerFilter(logging.Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loggers = os.getenv('LOGGERS', '')
        self.logger_keys = [l.strip() for l in loggers.split(',') if l.strip()]

        self.levelname = os.getenv('LOG_LEVEL', 'INFO')
        self.levelno = LEVEL_MAP.get(self.levelname, LEVEL_MAP['NOTSET'])

    def filter(self, record):
        if record.levelno < self.levelno:
            return False

        if record.name in self.logger_keys or not self.logger_keys:
            return True

        for key in self.logger_keys:
            size = len(key)
            if record.name.find(key, 0, size) != 0:
                continue

            if record.name[size] == '.':
                return True

        return False
