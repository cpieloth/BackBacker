import logging
import os
from subprocess import call

from backbacker.command import SystemCommand, CliCommand, Argument


__author__ = 'Christof Pieloth'

logger = logging.getLogger(__name__)


class MountSamba(SystemCommand):
    """Mounts a samba network share."""

    def __init__(self):
        super().__init__('mount')
        self._cfg = None
        self.url = None
        self._dst = None

    @property
    def cfg(self):
        return self._cfg

    @cfg.setter
    def cfg(self, value):
        self._cfg = os.path.expanduser(value)

    @property
    def dst(self):
        return self._dst

    @dst.setter
    def dst(self, value):
        self._dst = os.path.expanduser(value)

    def _execute_command(self):
        if not os.access(self.cfg, os.R_OK):
            raise PermissionError('No read access to: {}'.format(self.cfg))
        if not os.access(self.dst, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst))

        cmd = [self.cmd, '-t', 'cifs', '-o', 'credentials={}'.format(self.cfg), self.url, self.dst]
        if call(cmd) != 0:
            raise RuntimeError('Error calling: {}'.format(' '.join(cmd)))


class UMount(SystemCommand):
    """Unmounts a mounting point."""

    def __init__(self):
        super().__init__('umount')
        self._dir = None

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, value):
        self._dir = value

    def _execute_command(self):
        if not os.access(self.dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dir))

        cmd = [self.cmd, self.dir]
        if call(cmd) != 0:
            raise RuntimeError('Error calling: {}'.format(' '.join(cmd)))


class MountSambaCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.CONFIG_FILE.long_arg, help='Config file for .credentials.', required=True)
        parser.add_argument(Argument.URL.long_arg, help='URL of the samba share.', required=True)
        parser.add_argument(Argument.DST_DIR.long_arg, help='Mount directory.', required=True)

    @classmethod
    def _name(cls):
        return 'mount_smb'

    @classmethod
    def _help(cls):
        return MountSamba.__doc__

    @classmethod
    def _instance(cls, args):
        instance = MountSamba()
        instance.cfg = Argument.CONFIG_FILE.get_value(args)
        instance.url = Argument.URL.get_value(args)
        instance.dst = Argument.DST_DIR.get_value(args)
        return instance


class UmountCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.DIR.long_arg, help='Director to unmount.', required=True)

    @classmethod
    def _name(cls):
        return 'umount'

    @classmethod
    def _help(cls):
        return UMount.__doc__

    @classmethod
    def _instance(cls, args):
        instance = UMount()
        instance.dir = Argument.DIR.get_value(args)
        return instance
