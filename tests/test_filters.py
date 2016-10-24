from logging import LogRecord
import time

import pytest

from belogging.defaults import LEVEL_MAP
from belogging.exceptions import ConfigurationWarning
from belogging.filters import LoggerFilter, LoggerDuplicationFilter


def create_record(name='test_logger', level='DEBUG', msg='foobar'):
    return LogRecord(name=name, level=LEVEL_MAP[level], msg=msg, lineno=None,
                     args=None, exc_info=None, pathname=None)

# LoggerFilter


def test_filter_by_name(monkeypatch):
    monkeypatch.setenv('LOGGERS', 'test_logger')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')

    ft = LoggerFilter()
    assert ft.filter(create_record())
    assert ft.filter(create_record(name='unknown')) is False


def test_filter_name_unset(monkeypatch):
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')

    ft = LoggerFilter()
    assert ft.filter(create_record())
    assert ft.filter(create_record(name='unknown'))


def test_filter_name_hierarchy(monkeypatch):
    monkeypatch.setenv('LOGGERS', 'top.sub1,othertop')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')

    ft = LoggerFilter()
    assert ft.filter(create_record(name='top.sub1'))
    assert ft.filter(create_record(name='top')) is False
    assert ft.filter(create_record(name='othertop'))
    assert ft.filter(create_record(name='othertop.whatever'))


def test_filter_by_level(monkeypatch):
    monkeypatch.setenv('LOGGERS', 'test_logger')
    monkeypatch.setenv('LOG_LEVEL', 'ERROR')

    ft = LoggerFilter()
    assert ft.filter(create_record(level='DEBUG')) is False
    assert ft.filter(create_record(level='INFO')) is False
    assert ft.filter(create_record(level='ERROR')) is True
    assert ft.filter(create_record(level='CRITICAL')) is True


def test_filter_disabled_level(monkeypatch):
    monkeypatch.setenv('LOGGERS', 'test_logger')
    monkeypatch.setenv('LOG_LEVEL', 'DISABLED')

    ft = LoggerFilter()
    assert ft.filter(create_record(level='DEBUG')) is False
    assert ft.filter(create_record(level='CRITICAL')) is False


def test_filter_level_unset(monkeypatch):
    monkeypatch.setenv('LOGGERS', 'test_logger')

    ft = LoggerFilter()
    # INFO is set as default
    assert ft.filter(create_record(level='DEBUG')) is False
    assert ft.filter(create_record(level='INFO'))
    assert ft.filter(create_record(level='CRITICAL'))


# LoggerDuplicationFilter


def test_default_duplication_filter():
    ft = LoggerDuplicationFilter()
    ft.filter(create_record(msg='repeated')) is True
    ft.filter(create_record(msg='repeated')) is False
    ft.filter(create_record(msg='not repeated')) is True


@pytest.mark.slow
def test_duplication_filter_configuration_errors(monkeypatch):
    monkeypatch.setenv('LOG_CACHE_EXPIRE', 0)
    with pytest.raises(ConfigurationWarning):
        LoggerDuplicationFilter()

    monkeypatch.setenv('LOG_CACHE_SIZE', 0)
    with pytest.raises(ConfigurationWarning):
        LoggerDuplicationFilter()


@pytest.mark.slow
def test_duplication_filter_respect_expire_time_and_cache_size(monkeypatch):
    monkeypatch.setenv('LOG_CACHE_SIZE', 2)
    monkeypatch.setenv('LOG_CACHE_EXPIRE', 1)

    ft = LoggerDuplicationFilter()
    ft.filter(create_record(msg='repeated 1')) is True
    ft.filter(create_record(msg='repeated 2')) is True
    ft.filter(create_record(msg='repeated 1')) is False
    ft.filter(create_record(msg='repeated 2')) is False
    time.sleep(1)
    ft.filter(create_record(msg='repeated 1')) is True
    ft.filter(create_record(msg='repeated 2')) is True


def test_duplication_filter_cache_size(monkeypatch):
    monkeypatch.setenv('LOG_CACHE_SIZE', 1)

    ft = LoggerDuplicationFilter()
    ft.filter(create_record(msg='repeated 1')) is True
    ft.filter(create_record(msg='repeated 2')) is True
    ft.filter(create_record(msg='repeated 1')) is True
    ft.filter(create_record(msg='repeated 2')) is True
    ft.filter(create_record(msg='repeated 2')) is False
