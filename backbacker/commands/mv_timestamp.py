from datetime import datetime
import logging
import os
import shutil

from backbacker import command
from backbacker import constants


__author__ = 'Christof Pieloth'

logger = logging.getLogger(__name__)


class MoveTimestamp(command.Command):
    """Moves/renames all files in a folder to a destination by adding a timestamp prefix."""

    def __init__(self):
        super().__init__()
        self._src_dir = None
        self._dst_dir = None
        self.datefmt = constants.FILE_DATE_FORMAT

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
            logger.exception('Could not create date string for %s! Using default format %s',
                             self.datefmt, constants.FILE_DATE_FORMAT)
            date_str = datetime.now().strftime(constants.FILE_DATE_FORMAT)

        # Collecting file to avoid conflict if src_dir eq. dest_dir.
        files = []
        for entry in os.listdir(self.src_dir):
            file = os.path.join(self.src_dir, entry)
            if os.path.isfile(file):
                files.append(file)

        errors = 0
        for file_in in files:
            fname = os.path.basename(file_in)
            file_out = os.path.join(self.dst_dir, date_str + constants.DATE_PREFIX_SEPARATOR + fname)
            try:
                # Using shutil.move() instead of os.rename() to enable operation over different filesystems.
                shutil.move(file_in, file_out)
            except Exception:
                logger.exception('Could not move file: %s', file_in)
                errors += 1

        if errors > 0:
            raise RuntimeError('Could not move {} files.'.format(errors))


class MoveTimestampCliCommand(command.CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(command.Argument.SRC_DIR.long_arg, required=True,
                            help='Source directory which should be moved.')
        parser.add_argument(command.Argument.DST_DIR.long_arg, help='Destination directory.', required=True)
        parser.add_argument(command.Argument.DATE_FORMAT.long_arg, help='Date format for the timestamp prefix.',
                            default=constants.FILE_DATE_FORMAT)

    @classmethod
    def _name(cls):
        return 'mv_timestamp'

    @classmethod
    def _help(cls):
        return MoveTimestamp.__doc__

    @classmethod
    def _instance(cls, args):
        instance = MoveTimestamp()
        instance.src_dir = command.Argument.SRC_DIR.get_value(args)
        instance.dst_dir = command.Argument.DST_DIR.get_value(args)
        instance.datefmt = command.Argument.DATE_FORMAT.get_value(args)
        return instance
