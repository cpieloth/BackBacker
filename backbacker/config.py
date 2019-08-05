import configparser
import os

__author__ = 'Christof Pieloth'


class Config(object):

    def __init__(self):
        self._log = CfgLogging()

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
            if not files or len(files) == 0:
                IOError('Error on reading config file: %s'.format(fname))
                return cfg
            cfg.parse_cfg(cfg_parser)

        return cfg


class CfgLogging(object):

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
            raise ValueError('Unknown log type: %s'.format(value))

        self._type = value

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if value:
            self._file = os.path.expanduser(value)
