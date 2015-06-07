__author__ = 'Gunnar Nitsche'

from datetime import datetime
from glob import glob
import os
import sys

from backbacker.constants import Parameter
from backbacker.constants import Constants
from backbacker.errors import ParameterError

from .command import Command


class BackupRotation(Command):
    """Deletes old backups using a timestamp as rotation condition."""

    DATE_PREFIX_SEP = Constants.DATE_PREFIX_SEPARATOR

    def __init__(self):
        Command.__init__(self, 'backup_rotation')
        self.__arg_src = ''
        self.__arg_date_pattern = Constants.FILE_DATE_FORMAT
        self.__arg_keep_backups = Constants.KEEP_BACKUPS

    @property
    def arg_src(self):
        return self.__arg_src

    @arg_src.setter
    def arg_src(self, value):
        self.__arg_src = os.path.expanduser(value)

    @property
    def arg_date_pattern(self):
        return self.__arg_date_pattern

    @arg_date_pattern.setter
    def arg_date_pattern(self, pattern):
        self.__arg_date_pattern = pattern

    @property
    def arg_keep_backups(self):
        return self.__arg_keep_backups

    @arg_keep_backups.setter
    def arg_keep_backups(self, value):
        try:
            self.__arg_keep_backups = int(value)
        except ValueError:
            self.log.error('Could not cast to int: ' + str(value))
            self.__arg_keep_backups = sys.maxsize
        if self.__arg_keep_backups == 0:
            self.log.warn('rotation == 0 are ignored!')
            self.__arg_keep_backups = sys.maxsize

    def execute(self):
        if not os.access(self.arg_src, os.R_OK):
            self.log.error('No read access for: ' + self.arg_src)
            return False
        if not os.access(self.arg_src, os.W_OK):
            self.log.error('No write access for: ' + self.arg_src)
            return False

        dates = [x.split(BackupRotation.DATE_PREFIX_SEP)[0] for x in os.listdir(self.arg_src)
                 if os.path.isfile(os.path.join(self.arg_src, x))]
        dates = set(dates)
        dates = [datetime.strptime(x, self.arg_date_pattern) for x in dates]

        if len(dates) > self.arg_keep_backups:
            dates.sort()
            files = []

            for dpfx in dates[:-self.arg_keep_backups]:
                spfx = dpfx.strftime(self.arg_date_pattern) + BackupRotation.DATE_PREFIX_SEP + '*'
                files.extend(glob(os.path.join(self.arg_src, spfx)))

            for dfile in files:
                os.remove(dfile)

        return True

    @classmethod
    def instance(cls, params):
        cmd = BackupRotation()
        if Parameter.DIR in params:
            cmd.arg_src = params[Parameter.DIR]
        else:
            raise ParameterError(Parameter.DIR + ' parameter is missing!')

        if Parameter.ROTATE in params:
            cmd.arg_keep_backups = params[Parameter.ROTATE]
        else:
            cls.cls_log.warn('Rotate not specified! Using default: ' + Constants.KEEP_BACKUPS)

        if Parameter.DATE_FORMAT in params:
            cmd.arg_date_pattern = params[Parameter.DATE_FORMAT]
        else:
            cls.cls_log.warn('No date format defined! Using default: ' + cmd.arg_date_pattern)

        return cmd

    @classmethod
    def prototype(cls):
        return BackupRotation()
