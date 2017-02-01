config-logger: Configurable and flexible logger for your python applications
============================================================================

Build Status
------------

|travis status| |coverage| |health|

Project details
---------------

|license| |pypi|

.. |travis status| image:: https://travis-ci.org/afxentios/config-logger.svg?branch=master
   :target: https://travis-ci.org/afxentios/config-logger
   :alt: Travis-CI build status
.. |coverage| image:: https://coveralls.io/repos/github/afxentios/config-logger/badge.svg
   :target: https://coveralls.io/github/afxentios/config-logger
   :alt: Code Coverage
.. |health| image:: https://landscape.io/github/afxentios/config-logger/master/landscape.svg?style=flat
   :target: https://landscape.io/github/afxentios/config-logger/master
   :alt: Code Health
.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/afxentios/config-logger/blob/master/LICENSE.txt
   :alt: License
.. |pypi| image:: https://badge.fury.io/py/config-logger.svg
   :target: https://badge.fury.io/py/config-logger
   :alt: Pypi Version


Description
-----------

The **config-logger** package is a basic configurable logger. It reads the configuration data for the logging from an
external YAML, JSON file or from a given python dictionary and validates it. The contents of this dictionary are
described in `Configuration dictionary schema`_. This package is currently tested on Python 2.7.

- `Issue tracker`_
- `Changelog`_


Installation
------------

::

    pip install config-logger

or

download the `latest release`_ and run

::

    python setup.py install


Usage
-----

Configured from external .yaml or .json file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    #logging.yaml contains the configuration data which defines the logging in your project

    from config_logger import Logger
    logger = Logger(name='my_logger', cfg_path='/path/to/logging.yaml')
    logger.info("This will be written in a file called info.log")

**Console Output**

::

    2017-01-31 12:20:32,693 - my_logger - INFO - This will be written in a file called info.log

Configured from dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'basic': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                'level': 'WARNING',
                'stream': 'ext://sys.stdout'
            }
        'root': {
            'handlers': ['console'],
            'level': 'WARNING'
        }
    }

    from config_logger import Logger
    logger = Logger(name='my_logger', default_conf=log_config)
    logger.warning("This will be written in a file called warning.log")

**Console Output**

::

    2017-01-31 13:12:56,002 - my_logger - WARNING - This will be written in a file called warning.log

*Note: You can find sample of logging configuration files supported by config-logger in* `this repo`_.


License
-------

This project is licensed under the MIT license.

.. _Changelog: https://github.com/afxentios/config-logger/blob/master/CHANGELOG.md
.. _Issue tracker: https://github.com/afxentios/config-logger/issues
.. _latest release: https://github.com/afxentios/config-logger/releases
.. _Configuration dictionary schema: https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
.. _this repo: https://github.com/afxentios/python_logging_configuration_sample
