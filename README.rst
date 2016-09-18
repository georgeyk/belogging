Belogging
=========

|TravisCI Build Status| |Coverage Status|

----

Easy logging configuration based on environment variables.

Features:

    * Set logging level using environment variable LOG_LEVEL (defaults to 'INFO')
    * Set which loggers to enable using environment variable LOGGERS (defaults to '', everything)
    * Always output to stdout
    * Completely disable logging setting LOG_LEVEL=DISABLED

Requirements:

    * Python 3.5 and beyond


Examples:
---------

Simple applications:

.. code-block:: python

    # my_script.py

    import logging
    import belogging
    belogging.load()

    logger = logging.getLogger('foobar')
    logger.debug('test 1')
    logger.info('test 2')


Executing:

.. code-block:: bash

    # selecting LOG_LEVEL
    $ LOG_LEVEL=DEBUG python my_script.py

    # selecting LOGGERS
    $ LOGGERS=foobar python my_script.py

    # Both
    $ LOGGERS=foobar LOG_LEVEL=INFO my_script.py


Note:
-----

If you are developing a library you should not configure the logging.
Applications configure it, libraries only "log" messages.


.. |TravisCI Build Status| image:: https://travis-ci.org/georgeyk/belogging.svg?branch=master
   :target: https://travis-ci.org/georgeyk/belogging
.. |Coverage Status| image:: https://coveralls.io/repos/github/georgeyk/belogging/badge.svg?branch=master
   :target: https://coveralls.io/github/georgeyk/belogging?branch=master
