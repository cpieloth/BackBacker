from datetime import datetime
import logging
import os
import shutil

from backbacker.command import Command, CliCommand, Argument
from backbacker.constants import Constants


__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class MoveTimestamp(Command):
    """Moves/renames all files in a folder to a destination by adding a timestamp prefix."""

    def __init__(self):
        super().__init__()
        self._src_dir = None
        self._dst_dir = None
        self.datefmt = Constants.FILE_DATE_FORMAT

    @property
    def src_dir(self):
        return self._src_dir

    @src_dir.setter
    def src_dir(self, value):
        self._src_dir = os.path.expanduser(value)

    @property
    def dst_dir(self):
        return self._dst_dir

    @dst_dir.setter
    def dst_dir(self, value):
        self._dst_dir = os.path.expanduser(value)

    def execute(self):
        if not os.access(self.src_dir, os.R_OK):
            raise PermissionError('No read access to: {}'.format(self.src_dir))
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))

        try:
            date_str = datetime.now().strftime(self.datefmt)
        except Exception:
            log.exception('Could not create date string for %s! Using default format %s',
                          self.datefmt, Constants.FILE_DATE_FORMAT)
            date_str = datetime.now().strftime(Constants.FILE_DATE_FORMAT)

        # Collecting file to avoid conflict if src_dir eq. dest_dir.
        files = []
        for entry in os.listdir(self.src_dir):
            file = os.path.join(self.src_dir, entry)
            if os.path.isfile(file):
                files.append(file)

        errors = 0
        for file_in in files:
            fname = os.path.basename(file_in)
            file_out = os.path.join(self.dst_dir, date_str + Constants.DATE_PREFIX_SEPARATOR + fname)
            try:
                # Using shutil.move() instead of os.rename() to enable operation over different filesystems.
                shutil.move(file_in, file_out)
            except Exception:
                log.exception('Could not move file: %s', file_in)
                errors += 1

        if errors == 0:
            return True
        else:
            return False


class MoveTimestampCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        # TODO(cpieloth): improve help
        subparsers.add_argument(Argument.SRC_DIR.long_arg, help='source dir', required=True)
        subparsers.add_argument(Argument.DST_DIR.long_arg, help='destination dir', required=True)
        subparsers.add_argument(Argument.DATE_FORMAT.long_arg, help='date format',
                                default=Constants.FILE_DATE_FORMAT)

    @classmethod
    def _name(cls):
        return 'mv_timestamp'

    @classmethod
    def _help(cls):
        return MoveTimestamp.__doc__

    @classmethod
    def _instance(cls, args):
        instance = MoveTimestamp()
        instance.src_dir = Argument.SRC_DIR.get_value(args)
        instance.dst_dir = Argument.DST_DIR.get_value(args)
        instance.datefmt = Argument.DATE_FORMAT.get_value(args)
        return instance
