try:
    import unittest2 as unittest
except ImportError:
    import unittest

import logging

from config_manager import ConfigManager
from mock import patch
from testfixtures import log_capture

from config_logger import Logger


class LoggerTest(unittest.TestCase):
    config0 = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'basic': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'basic',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            'sut_logger': {
                'level': 'DEBUG',
                'handlers': ['console']
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'WARNING'
        }
    }

    config1 = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'basic': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'filters': {
            'info_special': {
                '()': 'config_logger.filters.SameLevelFilter',
                'level': 'logging.INFO',
            },
            'critical_special': {
                '()': 'config_logger.filters.LessEqualLevelFilter',
                'level': 'logging.CRITICAL',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                'level': 'DEBUG',
                'stream': 'ext://sys.stdout'
            },
            'critical_file_handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                'level': 'CRITICAL',
                'filters': ['critical_special'],
                'stream': 'ext://sys.stdout'
            },
            'error_file_handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                'level': 'ERROR',
                'stream': 'ext://sys.stdout'
            },
            'info_file_handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                'level': 'INFO',
                'filters': ['info_special'],
                'stream': 'ext://sys.stdout'
            },
            'warning_file_handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                'level': 'WARNING',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            'test_error_logger': {
                'handlers': ['error_file_handler'],
                'level': 'ERROR',
                'propagate': False
            }
        },
        'root': {
            'handlers': ['console', 'info_file_handler', 'error_file_handler'],
            'level': 'INFO'
        }
    }

    config2 = {
        'version': 1,
        'disable_existing_loggers': False,
        'root':
            {
                'level': 'WARNING'
            }
    }

    config3 = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'basic': {
                'format': '%(asctime)s - %(passed_argument_1)s - %(passed_argument_2)s - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'basic',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            'sut_logger': {
                'level': 'DEBUG',
                'handlers': ['console']
            },
        }
    }

    @patch.object(ConfigManager, 'load_config')
    def test_logger_constructor(self, mocked_config):
        # Given
        mocked_config.return_value = None
        name = 'test_error_logger'
        # When
        logger = Logger(name=name, default_conf=self.config1)
        # Then
        self.assertEqual(logger.logger.name, 'test_error_logger')
        self.assertEqual(logging.getLevelName(logger.logger.level), 'ERROR')
        self.assertEqual(logging.getLevelName(logger.logger.root.level), 'INFO')

    @patch.object(ConfigManager, 'load_config')
    def test_logger_constructor_logging_level(self, mocked_config):
        # Given
        mocked_config.return_value = None
        name = 'root_logger'
        default_level = logging.ERROR
        # When
        logger = Logger(name=name, default_level=default_level, default_conf=self.config2)
        # Then
        self.assertEqual(logger.logger.name, 'root_logger')
        self.assertEqual(logging.getLevelName(logger.logger.level), 'NOTSET')

    @patch.object(ConfigManager, 'load_config')
    def test_logger_constructor_logging_level_root_and_logger(self, mocked_config):
        # Given
        mocked_config.return_value = None
        name = 'sut_logger'
        # When
        logger = Logger(name=name, default_conf=self.config0)
        # Then
        self.assertEqual(logger.logger.name, 'sut_logger')
        self.assertEqual(logging.getLevelName(logger.logger.level), 'DEBUG')
        self.assertEqual(logging.getLevelName(logger.logger.root.level), 'WARNING')

    def test_logger_constructor_logging_level_when_incorrect_conf_file(self):
        # Given
        name = 'sut_logger'
        cfg_path = 'wrong/path.to/log_conf.yaml'
        # When
        logger = Logger(name=name, cfg_path=cfg_path)
        # Then
        self.assertEqual(logger.logger.name, 'sut_logger')
        self.assertEqual(logging.getLevelName(logger.logger.level), 'INFO')

    def test_logger_logging_level_and_root_level_when_ino_conf_file_specified(self):
        # Given
        name = 'sut_logger'
        # When
        logger = Logger(name=name, default_conf=self.config0)
        # Then
        self.assertEqual(logger.logger.name, 'sut_logger')
        self.assertEqual(logging.getLevelName(logger.logger.level), 'DEBUG')
        self.assertEqual(logging.getLevelName(logger.logger.root.level), 'WARNING')

    @patch.object(ConfigManager, 'load_config')
    @log_capture('sut_logger')
    def test_debug_logger(self, l, mocked_config):
        # Given
        mocked_config.return_value = None
        logger = Logger(name='sut_logger', default_conf=self.config1)
        # When
        logger.debug('a debug message')
        # Then
        l.check(('sut_logger', 'DEBUG', 'a debug message'))

    @patch.object(ConfigManager, 'load_config')
    @log_capture('root_logger')
    def test_info_logger(self, l, mocked_config):
        # Given
        mocked_config.return_value = None
        logger = Logger(name='root_logger', default_conf=self.config1)
        # When
        logger.info('a message')
        # Then
        l.check(('root_logger', 'INFO', 'a message'))

    @patch.object(ConfigManager, 'load_config')
    @log_capture('root_logger')
    def test_warning_logger(self, l, mocked_config):
        # Given
        mocked_config.return_value = None
        logger = Logger(name='root_logger', default_conf=self.config1)
        # When
        logger.warning('a warning')
        # Then
        l.check(('root_logger', 'WARNING', 'a warning'))

    @patch.object(ConfigManager, 'load_config')
    @log_capture('root_logger')
    def test_error_logger(self, l, mocked_config):
        # Given
        mocked_config.return_value = None
        logger = Logger(name='root_logger', default_conf=self.config1)
        # When
        logger.error('an error')
        # Then
        l.check(('root_logger', 'ERROR', 'an error'))

    @patch.object(ConfigManager, 'load_config')
    @log_capture('root_logger')
    def test_critical_logger(self, l, mocked_config):
        # Given
        mocked_config.return_value = None
        logger = Logger(name='root_logger', default_conf=self.config1)
        # When
        logger.critical('a critical error')
        # Then
        l.check(('root_logger', 'CRITICAL', 'a critical error'))

    @patch.object(ConfigManager, 'load_config')
    def test_extra_parameters_passed(self, mocked_config):
        # Given
        mocked_config.return_value = None
        name = 'sut_logger'
        # When
        logger = Logger(name=name, default_conf=self.config3, extra={'passed_argument_1': 'A contextual info',
                                                                     'passed_argument_2': 'Another contextual info'})
        # Then
        self.assertEqual(logger.logger.logger.handlers[0].formatter._fmt,
                         '%(asctime)s - %(passed_argument_1)s - %(passed_argument_2)s - %(levelname)s - %(message)s')
        self.assertEqual(logger.logger.logger.name, 'sut_logger')
        self.assertEqual(logging.getLevelName(logger.logger.logger.level), 'DEBUG')
