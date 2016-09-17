# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from unittest import mock

from belogging.loader import BeloggingLoader


def test_loader_init():
    loader = BeloggingLoader(log_format='%(foobar)s')
    assert loader.config['formatters']['default']['format'] == '%(foobar)s'

    with mock.patch('logging.captureWarnings') as mocked_logging:
        loader = BeloggingLoader(capture_warnings=False)
        assert mocked_logging.called


def test_update_default_formatter():
    loader = BeloggingLoader()
    loader.update_default_formatter('%(foobar)s')
    assert loader.config['formatters']['default']['format'] == '%(foobar)s'


def test_setup():
    loader = BeloggingLoader()
    with mock.patch('logging.config.dictConfig') as mocked_config:
        configured = loader.setup()
        assert configured
        assert mocked_config.called
