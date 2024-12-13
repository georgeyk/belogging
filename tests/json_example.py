import logging

from belogging.loader import BeloggingLoader

loader = BeloggingLoader(json=True)
loader.setup()


logger = logging.getLogger("foo")
logger.info("foo")
