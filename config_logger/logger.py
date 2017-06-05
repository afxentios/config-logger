import logging
import os
from logging.config import dictConfig

try:
    from config_manager import ConfigManager, FileFormatError
except ImportError:
    print (
        "[-] The config_manager module is needed to read the logging configurations.\nDo `pip install config_manager`")
    raise


class Logger(object):
    def __init__(
            self,
            name,
            cfg_path=None,
            default_level=logging.INFO,
            default_conf=None,
            extra=None,
            env_key='CONF_PATH'
    ):
        """Create and initialize a Logger object.

            parameters:
                name - Name of the Logger instance.
                cfg_path - Path of the logging configuration file.
                default_level - Default logging level.
                default_conf - Dictionary with the default values for the config files.
                env_key - Environment variable which can be set to load the logging configuration from specific path.

        """
        self.name = name
        self.cfg_path = cfg_path
        self.default_level = default_level
        self.default_conf = default_conf
        self.env_key = env_key
        self.extra = extra
        self.logger = self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration

        """
        path = os.getenv(self.env_key, None) or self.cfg_path
        try:
            config = ConfigManager(config_file_path=path, defaults=self.default_conf,
                                   required=['version']) if self.cfg_path else self.default_conf
            dictConfig(config)
            logger = logging.getLogger(self.name)
        except (ValueError, IOError, FileFormatError):
            logging.basicConfig(level=self.default_level)
            logger = logging.getLogger(self.name)
            logger.setLevel(self.default_level)

        if self.extra:
            logger = logging.LoggerAdapter(logger, self.extra)

        return logger

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
