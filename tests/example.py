import logging

from belogging.loader import BeloggingLoader

loader = BeloggingLoader()
loader.setup()


logger = logging.getLogger("foo")
logger.debug("foo debug")
logger.info("foo info")


logger2 = logging.getLogger("foo.bar")
logger2.debug("foo.bar debug")
logger2.info("foo.bar info")


logger3 = logging.getLogger("bar")
logger2.debug("bar debug")
logger2.error("bar error")
