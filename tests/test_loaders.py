from unittest import mock

import pytest

from belogging import load
from belogging.defaults import DEFAULT_KVP_FORMAT
from belogging.exceptions import ConfigurationWarning
from belogging.loader import BeloggingLoader


def test_loader_init():
    with mock.patch("logging.captureWarnings") as mocked_logging:
        loader = BeloggingLoader(capture_warnings=False)
        assert loader.config["formatters"]["default"]["format"] == DEFAULT_KVP_FORMAT
        assert mocked_logging.called
        mocked_logging.assert_called_once_with(False)


def test_without_kvp_format():
    loader = BeloggingLoader(use_default_kvp=False)
    assert loader.config["formatters"]["default"]["format"] != DEFAULT_KVP_FORMAT


def test_update_default_formatter():
    loader = BeloggingLoader()
    loader.update_default_formatter("%(foobar)s")
    assert loader.config["formatters"]["default"]["format"] == "%(foobar)s"


def test_enable_json():
    loader = BeloggingLoader(json=True)
    assert "json" in loader.config["formatters"]
    assert loader.config["formatters"]["json"]
    assert loader.config["handlers"]["default"]["formatter"] == "json"


def test_add_filter():
    loader = BeloggingLoader()
    loader.add_filter("foobar", "whatever.path.ToFilter")
    assert "foobar" in loader.config["filters"]
    assert "foobar" in loader.config["handlers"]["default"]["filters"]


def test_add_filter_twice():
    loader = BeloggingLoader()
    loader.add_filter("foobar", "whatever.path.ToFilter")
    with pytest.raises(ConfigurationWarning):
        loader.add_filter("foobar", "whatever.path.ToFilter")


def test_setup():
    loader = BeloggingLoader()
    with mock.patch("logging.config.dictConfig") as mocked_config:
        configured = loader.setup()
        assert configured
        assert mocked_config.called


#
# load sugar
#


def test_load_log_format():
    configured = load(log_format="%(foobar)s")
    assert configured["formatters"]["default"]["format"] == "%(foobar)s"


def test_enable_duplication_filter_default():
    configured = load()
    assert "logger_duplication" not in configured["filters"]


def test_enable_duplication_filter():
    configured = load(enable_duplication_filter=True)
    assert "logger_duplication" in configured["filters"]
