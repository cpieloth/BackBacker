from datetime import datetime
import logging
from glob import glob
import os
import sys

from backbacker.command import Command, CliCommand, Argument
from backbacker.constants import Constants


__author__ = 'Gunnar Nitsche'

logger = logging.getLogger(__name__)


class BackupRotation(Command):
    """Deletes old backups using a timestamp as rotation condition."""

    DATE_PREFIX_SEP = Constants.DATE_PREFIX_SEPARATOR

    def __init__(self):
        super().__init__()
        self._dir = None
        self.date_pattern = Constants.FILE_DATE_FORMAT
        self._keep_backups = sys.maxsize

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, value):
        self._dir = os.path.expanduser(value)

    @property
    def keep_backups(self):
        return self._keep_backups

    @keep_backups.setter
    def keep_backups(self, value):
        try:
            self._keep_backups = int(value)
        except ValueError:
            raise ValueError('Could not cast "keep_backups" to int: {}'.format(value))

        if self._keep_backups <= 0:
            raise ValueError('Invalid value of "keep_backups". Must be greater than 0, but it is: {}'.format(value))

    def execute(self):
        if not os.access(self.dir, os.R_OK):
            raise PermissionError('No read access to: {}'.format(self.dir))
        if not os.access(self.dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dir))

        dates = [x.split(BackupRotation.DATE_PREFIX_SEP)[0] for x in os.listdir(self.dir)
                 if os.path.isfile(os.path.join(self.dir, x))]
        dates = set(dates)
        dates = [datetime.strptime(x, self.date_pattern) for x in dates]

        if len(dates) > self.keep_backups:
            dates.sort()
            files = []

            for dpfx in dates[:-self.keep_backups]:
                spfx = dpfx.strftime(self.date_pattern) + BackupRotation.DATE_PREFIX_SEP + '*'
                files.extend(glob(os.path.join(self.dir, spfx)))

            for dfile in files:
                os.remove(dfile)


class BackupRotationCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.DIR.long_arg, required=True,
                            help='Directory which contains the backups with a date prefix.')
        parser.add_argument(Argument.DATE_FORMAT.long_arg, default=Constants.FILE_DATE_FORMAT,
                            help='Date format of the date prefix.')
        parser.add_argument(Argument.ROTATE.long_arg, type=int, default=5,
                            help='Number of backups to keep.')

    @classmethod
    def _name(cls):
        return 'backup_rotation'

    @classmethod
    def _help(cls):
        return BackupRotation.__doc__

    @classmethod
    def _instance(cls, args):
        instance = BackupRotation()
        instance.dir = Argument.DIR.get_value(args)
        if Argument.DATE_FORMAT.has_value(args):
            instance.date_pattern = Argument.DATE_FORMAT.get_value(args)
        if Argument.ROTATE.has_value(args):
            instance.keep_backups = Argument.ROTATE.get_value(args)
        return instance
