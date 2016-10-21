Belogging
=========

*Don't fight with logging ...*

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
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # my_script.py

    import belogging
    belogging.load()  # this call is optional, only useful for customization

    # belogging.getLogger is just a sugar to logging.getLogger, you can
    # use logging.getLogger as usual (and recommended).
    logger = belogging.getLogger('foobar')
    logger.debug('test 1')
    logger.info('test 2')


Executing:

.. code-block:: bash

    # selecting LOG_LEVEL
    $ LOG_LEVEL=DEBUG python my_script.py
    # level=DEBUG message=test 1
    # level=INFO message=test 2

    # selecting LOGGERS
    $ LOGGERS=foobar python my_script.py
    # Both messages

    # Both
    $ LOGGERS=foobar LOG_LEVEL=INFO my_script.py
    # only level=INFO message=test 2


Applications should call ```belogging.load()``` upon initialization.
The first ```__init__.py``` would be a good candidate, but anything before any call to
```logging``` module will be fine.


Django:
~~~~~~~


In your projects ```settings.py```:

.. code-block:: python

    import belogging
    # ... settings ...
    LOGGING = belogging.load()


Inside your code, just use ```logging.getLogger()``` as usual.

.. code-block:: bash

    $ export LOG_LEVEL=WARNING
    $ ./manage.py runserver
    # It will output only logging messages with severity > WARNING


Logging follows a hierarchy, so you easily select or skip some logging messages:


.. code-block:: bash

    $ export LOGGERS=my_app.critical_a,my_app.critical_c,my_lib
    $ ./my-app.py
    # "my_app.critical_b messages" will be skipped
    # all messages from my_lib will show up


Note:
-----

If you are developing a library you should not configure logging.
Applications configure it, libraries only "log" messages.


.. |TravisCI Build Status| image:: https://travis-ci.org/georgeyk/belogging.svg?branch=master
   :target: https://travis-ci.org/georgeyk/belogging
.. |Coverage Status| image:: https://coveralls.io/repos/github/georgeyk/belogging/badge.svg?branch=master
   :target: https://coveralls.io/github/georgeyk/belogging?branch=master
