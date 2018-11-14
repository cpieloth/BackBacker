import logging
import os
import subprocess

from backbacker import command

__author__ = 'Christof Pieloth'

logger = logging.getLogger(__name__)


class Rsync(command.SystemCommand):
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


class RsyncCliCommand(command.CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(command.Argument.SRC_DIR.long_arg, help='Source directory for sync.', required=True)
        parser.add_argument(command.Argument.DST_DIR.long_arg, help='Destination directory for sync.', required=True)
        parser.add_argument(command.Argument.BACKUP_DIR.long_arg, help='Backup directory for rsync.')
        parser.add_argument(command.Argument.MIRROR.long_arg, help='Enable mirror mode.', action='store_true')
        parser.add_argument(command.Argument.SHELL.long_arg, help='Remote shell to use.')

    @classmethod
    def _name(cls):
        return 'rsync'

    @classmethod
    def _help(cls):
        return Rsync.__doc__

    @classmethod
    def _instance(cls, args):
        instance = Rsync()
        instance.src_dir = command.Argument.SRC_DIR.get_value(args)
        instance.dst_dir = command.Argument.DST_DIR.get_value(args)
        instance.mirror = command.Argument.MIRROR.get_value(args)

        if command.Argument.BACKUP_DIR.has_value(args):
            instance.backup_dir = command.Argument.BACKUP_DIR.get_value(args)

        if command.Argument.SHELL.has_value(args):
            instance.rsh = command.Argument.SHELL.get_value(args)

        return instance
