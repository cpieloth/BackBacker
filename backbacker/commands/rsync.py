import logging
import os
import subprocess

from backbacker.command import SystemCommand, CliCommand
from backbacker.constants import Parameter


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
        subparsers.add_argument('--{}'.format(Parameter.SRC_DIR), help='source dir', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DST_DIR), help='destination dir', required=True)
        subparsers.add_argument('--{}'.format(Parameter.BACKUP_DIR), help='backup dir')
        subparsers.add_argument('--{}'.format(Parameter.MIRROR), help='mirror', action='store_true')
        subparsers.add_argument('--{}'.format(Parameter.SHELL), help='shell')

    @classmethod
    def _name(cls):
        return 'rsync'

    @classmethod
    def _help(cls):
        return Rsync.__doc__

    @classmethod
    def _instance(cls, args):
        instance = Rsync()
        instance.src_dir = args[Parameter.SRC_DIR]
        instance.dst_dir = args[Parameter.DST_DIR]
        instance.mirror = args[Parameter.MIRROR]

        if Parameter.BACKUP_DIR in args:
            instance.backup_dir = args[Parameter.BACKUP_DIR]

        if Parameter.SHELL in args:
            instance.rsh = args[Parameter.SHELL]

        return instance
