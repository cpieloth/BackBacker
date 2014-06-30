__author__ = 'Christof Pieloth'

import logging
import sys


class Config:
    """Stores global settings."""
    PARAM_LOG_TYPE = 'log_type'
    ARG_LOG_TYPE_CONSOLE = 'console'
    ARG_LOG_TYPE_FILE = 'file'

    PARAM_LOG_FILE = 'log_file'

    LOG_FORMAT_CONSOLE = '[%(levelname)s] %(name)s: %(message)s'
    LOG_FORMAT_FILE = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    LOG_FORMAT_DATE = "%Y-%m-%dT%H:%M:%S"

    def __init__(self):
        self._log_type = Config.ARG_LOG_TYPE_CONSOLE
        self._log_file = ''
        self._log_format = Config.LOG_FORMAT_CONSOLE
        self._log_datefmt = Config.LOG_FORMAT_DATE

    @property
    def log_datefmt(self):
        return self._log_datefmt

    @property
    def log_format(self):
        return self._log_format

    @log_format.setter
    def log_format(self, value):
        self.log_format = value

    @property
    def log_type(self):
        return self._log_type

    @log_type.setter
    def log_type(self, value):
        if value == Config.ARG_LOG_TYPE_CONSOLE:
            self._log_type = value
        elif value == Config.ARG_LOG_TYPE_FILE:
            self._log_type = value

    @property
    def log_file(self):
        return self._log_file

    @log_file.setter
    def log_file(self, value):
        self._log_file = value

    def apply_logging(self):
        """Initializes the logging."""
        if self.log_type == Config.ARG_LOG_TYPE_CONSOLE:
            self.log_format = Config.LOG_FORMAT_CONSOLE
            logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=self.log_format,
                                datefmt=self.log_datefmt)
        elif self.log_type == Config.ARG_LOG_TYPE_FILE:
            self.log_format = Config.LOG_FORMAT_FILE
            logging.basicConfig(level=logging.DEBUG, filename=self.log_file, format=self.log_format,
                                datefmt=self.log_datefmt)

    @staticmethod
    def read_config(fname):
        """Reads and creates a config from a file."""
        cfg = Config()
        cfg_file = None
        try:
            cfg_file = open(fname, 'r')

            for line in cfg_file:
                if line[0] == '#':
                    continue
                pair = line.split('=')
                if len(pair) != 2:
                    print('Could not read config line:\n' + str(line))
                    continue
                param = pair[0].lower().strip()
                arg = pair[1].strip()
                if param == Config.PARAM_LOG_TYPE:
                    cfg.log_type = arg
                elif param == Config.PARAM_LOG_FILE:
                    cfg.log_file = arg
                else:
                    print('Unknown property: ' + str(param))
        except IOError as err:
            print('Error on reading config file!\n' + str(err))
        finally:
            if cfg_file:
                cfg_file.close()
        return cfg