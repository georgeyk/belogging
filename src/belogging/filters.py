import logging
import os
from collections import OrderedDict
from datetime import datetime, timezone
from threading import Lock

from .defaults import LEVEL_MAP
from .exceptions import ConfigurationWarning


class LoggerFilter(logging.Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loggers = os.getenv("LOGGERS", "")
        self.logger_keys = [key.strip() for key in loggers.split(",") if key.strip()]

        self.levelname = os.getenv("LOG_LEVEL", "INFO")
        self.levelno = LEVEL_MAP.get(self.levelname, LEVEL_MAP["NOTSET"])

    def filter(self, record):
        if record.levelno < self.levelno:
            return False

        if record.name in self.logger_keys or not self.logger_keys:
            return True

        for key in self.logger_keys:
            size = len(key)
            if record.name.find(key, 0, size) != 0:
                continue

            if record.name[size] == ".":
                return True

        return False


class LoggerDuplicationFilter(logging.Filter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = Lock()

        self._cache_size = int(os.getenv("LOG_CACHE_SIZE", 32))
        if self._cache_size <= 0:
            msg = "LOG_CACHE_SIZE must be greater than 0, found={}".format(
                self._cache_size
            )
            raise ConfigurationWarning(msg)

        self._cache_expire = int(os.getenv("LOG_CACHE_EXPIRE", 10))
        if self._cache_expire <= 0:
            msg = "LOG_CACHE_EXPIRE must be greater than 0, found={}".format(
                self._cache_expire
            )
            raise ConfigurationWarning(msg)

        self._cache = OrderedDict({})

    def filter(self, record):
        msg = record.getMessage()
        with self.lock:
            if msg in self._cache:
                now = datetime.now(timezone.utc)
                delta = now - self._cache[msg]["time"]
                if delta.seconds >= self._cache_expire:
                    self._cache[msg]["time"] = now
                    self._cache[msg]["hits"] = 10
                    return True

                self._cache[msg]["hits"] += 1
                return False

        if len(self._cache) >= self._cache_size:
            # oldest key with less hits
            with self.lock:
                key, _ = sorted(self._cache.items(), key=lambda t: t[1]["hits"])[0]
                self._cache.pop(key, None)

        with self.lock:
            self._cache[msg] = {"time": datetime.now(timezone.utc), "hits": 0}

        return True
