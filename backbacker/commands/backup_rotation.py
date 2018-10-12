from datetime import datetime
import logging
from glob import glob
import os
import sys

from backbacker.command import Command, CliCommand
from backbacker.constants import Parameter
from backbacker.constants import Constants


__author__ = 'Gunnar Nitsche'

log = logging.getLogger(__name__)


class BackupRotation(Command):
    """Deletes old backups using a timestamp as rotation condition."""

    DATE_PREFIX_SEP = Constants.DATE_PREFIX_SEPARATOR

    def __init__(self):
        super().__init__()
        self._dir = None
        self.date_pattern = Constants.FILE_DATE_FORMAT
        self._keep_backups = Constants.KEEP_BACKUPS

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
            log.error('Could not cast to int: %s', value)
            self._keep_backups = sys.maxsize
        if self._keep_backups == 0:
            log.warning('rotation == 0 are ignored!')
            self._keep_backups = sys.maxsize

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

        return True


class BackupRotationCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        # TODO(cpieloth): improve help
        subparsers.add_argument('--{}'.format(Parameter.DIR), help='dir', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DATE_FORMAT), help='date format',
                                default=Constants.FILE_DATE_FORMAT)
        subparsers.add_argument('--{}'.format(Parameter.ROTATE), help='rotate', type=int,
                                default=Constants.KEEP_BACKUPS)

    @classmethod
    def _name(cls):
        return 'backup_rotation'

    @classmethod
    def _help(cls):
        return BackupRotation.__doc__

    @classmethod
    def _instance(cls, args):
        instance = BackupRotation()
        instance.dir = args[Parameter.DIR]
        if Parameter.DATE_FORMAT in args:
            instance.date_pattern = args[Parameter.DATE_FORMAT]
        if Parameter.ROTATE in args:
            instance.keep_backups = args[Parameter.ROTATE]
        return instance
