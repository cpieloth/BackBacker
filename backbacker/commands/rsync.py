import logging
import os
import subprocess

from backbacker.command import SystemCommand, CliCommand, Argument

__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class Rsync(SystemCommand):
    """
    Wrapper for rsync.
    rsync is a file transfer program capable of efficient remote update via a fast differencing algorithm.
    """

    ALL = '-a'  # -r -l -p -t -g -o -D
    DELETE_DEST = '--delete'
    BACKUP_DELETE = '-b'
    BACKUP_DELETE_DIR = '--backup-dir='
    REMOTE_SHELL = '-e'

    def __init__(self):
        super().__init__('rsync')
        self._src_dir = ''
        self._dst_dir = ''
        self._backup_dir = ''
        self.mirror = False
        self.rsh = ''

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

    @property
    def backup_dir(self):
        return self._backup_dir

    @backup_dir.setter
    def backup_dir(self, value):
        self._backup_dir = os.path.expanduser(value)

    def _execute_command(self):
        if self.rsh == '':
            if not os.access(self.src_dir, os.R_OK):
                raise PermissionError('No read access to: {}'.format(self.src_dir))
            if not os.access(self.dst_dir, os.W_OK):
                raise PermissionError('No write access to: {}'.format(self.dst_dir))

        cmd = [self.cmd, Rsync.ALL]
        if self.mirror:
            cmd.append(Rsync.DELETE_DEST)
            if self.backup_dir != '':
                cmd.append(Rsync.BACKUP_DELETE)
                cmd.append(Rsync.BACKUP_DELETE_DIR + self.backup_dir)
        if self.rsh != '':
            cmd.append(Rsync.REMOTE_SHELL + ' ' + self.rsh)
        cmd.append(self.src_dir)
        cmd.append(self.dst_dir)

        subprocess.check_call(cmd)


class RsyncCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        # TODO(cpieloth): improve help
        subparsers.add_argument(Argument.SRC_DIR.long_arg, help='source dir', required=True)
        subparsers.add_argument(Argument.DST_DIR.long_arg, help='destination dir', required=True)
        subparsers.add_argument(Argument.BACKUP_DIR.long_arg, help='backup dir')
        subparsers.add_argument(Argument.MIRROR.long_arg, help='mirror', action='store_true')
        subparsers.add_argument(Argument.SHELL.long_arg, help='shell')

    @classmethod
    def _name(cls):
        return 'rsync'

    @classmethod
    def _help(cls):
        return Rsync.__doc__

    @classmethod
    def _instance(cls, args):
        instance = Rsync()
        instance.src_dir = Argument.SRC_DIR.get_value(args)
        instance.dst_dir = Argument.DST_DIR.get_value(args)
        instance.mirror = Argument.MIRROR.get_value(args)

        if Argument.BACKUP_DIR.has_value(args):
            instance.backup_dir = Argument.BACKUP_DIR.get_value(args)

        if Argument.SHELL.has_value(args):
            instance.rsh = Argument.SHELL.get_value(args)

        return instance
