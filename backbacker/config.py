__author__ = 'Christof Pieloth'

import configparser
import os
import sys


class Config(object):
    """Stores global settings."""
    SECTION_LOGGING = 'logging'

    PARAM_LOG_TYPE = 'log_type'
    ARG_LOG_TYPE_CONSOLE = 'console'
    ARG_LOG_TYPE_FILE = 'file'

    PARAM_LOG_FILE = 'log_file'
    DEFAULT_LOG_FILE = '/tmp/backbacker.log'

    LOG_FORMAT_CONSOLE = '[%(levelname)s] %(name)s: %(message)s'
    LOG_FORMAT_FILE = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    LOG_FORMAT_DATE = "%Y-%m-%dT%H:%M:%S"

    def __init__(self):
        self.__log_type = Config.ARG_LOG_TYPE_CONSOLE
        self.__log_file = ''
        self.__log_format = Config.LOG_FORMAT_CONSOLE
        self.__log_datefmt = Config.LOG_FORMAT_DATE

    @property
    def log_datefmt(self):
        return self.__log_datefmt

    @property
    def log_format(self):
        return self.__log_format

    @log_format.setter
    def log_format(self, value):
        self.__log_format = value

    @property
    def log_type(self):
        return self.__log_type

    @log_type.setter
    def log_type(self, value):
        value = value.lower().strip()
        self.__log_type = value
        if self.log_type == Config.ARG_LOG_TYPE_CONSOLE:
            self.log_format = Config.LOG_FORMAT_CONSOLE
        elif self.log_type == Config.ARG_LOG_TYPE_FILE:
            self.log_format = Config.LOG_FORMAT_FILE
        else:
            self.log_type = Config.ARG_LOG_TYPE_CONSOLE
            print('Unknown log type! Logging to console instead.', file=sys.stderr)

    @property
    def log_file(self):
        return self.__log_file

    @log_file.setter
    def log_file(self, value):
        self.__log_file = os.path.expanduser(value)

    @staticmethod
    def read_config(fname):
        """Reads and creates a config from a file."""
        cfg = Config()

        cfg_parser = configparser.ConfigParser()
        files = cfg_parser.read(fname)
        if not files or len(files) == 0:
            print('Error on reading config file!', file=sys.stderr)
            return cfg

        cfg.log_type = cfg_parser.get(Config.SECTION_LOGGING, Config.PARAM_LOG_TYPE, fallback=Config.ARG_LOG_TYPE_CONSOLE)
        cfg.log_file = cfg_parser.get(Config.SECTION_LOGGING, Config.PARAM_LOG_FILE, fallback=Config.DEFAULT_LOG_FILE)

        return cfg
