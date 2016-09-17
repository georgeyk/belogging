# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import logging

from belogging.loader import BeloggingLoader


loader = BeloggingLoader()
loader.setup()


logger = logging.getLogger('foo')
logger.debug('debug')
logger.info('info')
logger.error('error')
logger.warning('warning')
logger.critical('critical')


logger2 = logging.getLogger('foo.bar')
logger2.debug('debug')
logger2.info('info')
logger2.error('error')
logger2.warning('warning')
logger2.critical('critical')
