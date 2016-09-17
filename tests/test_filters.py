# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from logging import LogRecord

from belogging.defaults import LEVEL_MAP
from belogging.filters import LoggerFilter


def create_record(name='test_logger', level='DEBUG', msg='foobar'):
    return LogRecord(name=name, level=LEVEL_MAP[level], msg=msg, lineno=None,
                     args=None, exc_info=None, pathname=None)


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
