import configparser
import os

__author__ = 'Christof Pieloth'


class Config:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.__init__(False)
        return cls.__instance

    def __init__(self, initialized=True):
        if not initialized:
            self._log = _CfgLogging()

    def parse_cfg(self, parser):
        self.log.parse_cfg(parser)

    @property
    def log(self):
        return self._log

    @classmethod
    def read_config(cls, fname):
        """Reads and creates a config from a file."""
        cfg = cls()

        if fname:
            cfg_parser = configparser.ConfigParser()
            files = cfg_parser.read(fname)
            if not files:
                raise IOError('Error on reading config file: {}'.format(fname))
            cfg.parse_cfg(cfg_parser)

        return cfg


class _CfgLogging:

    CFG_SECTION = 'logging'

    TYPE_CONSOLE = 'console'
    TYPE_FILE = 'file'

    FORMAT_CONSOLE = '[%(levelname)s] %(name)s: %(message)s'
    FORMAT_FILE = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    FORMAT_DATE = '%Y-%m-%dT%H:%M:%S'

    def __init__(self):
        self.format = self.FORMAT_CONSOLE
        self.datefmt = self.FORMAT_DATE
        self._type = self.TYPE_CONSOLE
        self._file = None

    def parse_cfg(self, parser, section=CFG_SECTION):
        self.type = parser.get(section, 'log_type', fallback=self.type)
        self.format = parser.get(section, 'log_format', fallback=self.format)
        self.datefmt = parser.get(section, 'log_datefmt', fallback=self.datefmt)
        self.file = parser.get(section, 'log_file', fallback=self.file)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        value = value.lower().strip()
        if value == self.TYPE_CONSOLE:
            self.format = self.FORMAT_CONSOLE
        elif value == self.TYPE_FILE:
            self.format = self.FORMAT_FILE
        else:
            raise ValueError('Unknown log type: {}'.format(value))

        self._type = value

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if value:
            self._file = os.path.expanduser(value)
