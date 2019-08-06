import abc
import logging
import os
import subprocess

from backbacker.command import SystemCommand, CliCommand, Argument

__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class FileSync(SystemCommand, metaclass=abc.ABCMeta):
    """
    Abstract base class for file sync commands, which provides an interface on API level.
    """

    def __init__(self, cmd):
        super().__init__(cmd)
        self._src_dir = ''
        self._dst_dir = ''
        self.mirror = False

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


class FileSyncCliCommand(CliCommand, metaclass=abc.ABCMeta):
    """Abstract base class for file sync commands, which provides an interface on CLI level."""

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.SRC_DIR.long_arg, help='Source directory for sync.', required=True)
        parser.add_argument(Argument.DST_DIR.long_arg, help='Destination directory for sync.', required=True)
        parser.add_argument(Argument.MIRROR.long_arg, help='Enable mirror mode.', action='store_true')


class Robocopy(FileSync):
    """
    Wrapper for robocopy.
    robocopy is a file transfer program for Windows.
    """

    MIRROR = '/MIR'

    def __init__(self):
        super().__init__('robocopy')

    def _execute_command(self):
        if not os.access(self.src_dir, os.R_OK):
            raise PermissionError('No read access to: {}'.format(self.src_dir))
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))

        cmd = [self.cmd, self.src_dir, self.dst_dir]
        if self.mirror:
            cmd.append(self.MIRROR)

        rc = subprocess.call(cmd)
        # https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy
        # https://ss64.com/nt/robocopy-exit.html
        if rc >= 16:
            raise RuntimeError('Error, no files were copied!')
        elif rc >= 4:
            raise RuntimeError('Check output, mismatch or some files are not copied!')

    @classmethod
    def check_version(cls, cmd):
        """
        Checks if  'cmd /?' is callable.

        :return True 'cmd /?' raises no exception
        """
        import subprocess
        try:
            subprocess.Popen([cmd, '/?'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except OSError:
            return False


class RobocopyCliCommand(FileSyncCliCommand):

    @classmethod
    def _name(cls):
        return 'robocopy'

    @classmethod
    def _help(cls):
        return Robocopy.__doc__

    @classmethod
    def _instance(cls, args):
        instance = Robocopy()
        instance.src_dir = Argument.SRC_DIR.get_value(args)
        instance.dst_dir = Argument.DST_DIR.get_value(args)
        instance.mirror = Argument.MIRROR.get_value(args)

        return instance


class Rsync(FileSync):
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
        self._backup_dir = ''
        self.rsh = ''

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

        cmd = [self.cmd, self.ALL]
        if self.mirror:
            cmd.append(self.DELETE_DEST)
            if self.backup_dir != '':
                cmd.append(self.BACKUP_DELETE)
                cmd.append(self.BACKUP_DELETE_DIR + self.backup_dir)
        if self.rsh != '':
            cmd.append(self.REMOTE_SHELL + ' ' + self.rsh)
        cmd.append(self.src_dir)
        cmd.append(self.dst_dir)

        subprocess.check_call(cmd)


class RsyncCliCommand(FileSyncCliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        FileSyncCliCommand._add_arguments(parser)
        parser.add_argument(Argument.BACKUP_DIR.long_arg, help='Backup directory for rsync.')
        parser.add_argument(Argument.SHELL.long_arg, help='Remote shell to use.')

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
