__author__ = 'Christof Pieloth'

import os
from subprocess import call
from backbacker.commands.command import SystemCommand
from backbacker.constants import Parameter
from backbacker.errors import ParameterError


class MountSamba(SystemCommand):
    """Mounts a samba network share."""

    def __init__(self):
        SystemCommand.__init__(self, 'mount_smb', 'mount')
        self.__arg_cfg = ''
        self.__arg_url = ''
        self.__arg_dest = ''

    @property
    def arg_cfg(self):
        return self.__arg_cfg

    @arg_cfg.setter
    def arg_cfg(self, value):
        self.__arg_cfg = value

    @property
    def arg_url(self):
        return self.__arg_url

    @arg_url.setter
    def arg_url(self, value):
        self.__arg_url = value

    @property
    def arg_dest(self):
        return self.__arg_dest

    @arg_dest.setter
    def arg_dest(self, value):
        self.__arg_dest = value

    def _execute_command(self):
        if not os.access(self.arg_cfg, os.R_OK):
            self.log.error('No read access to: ' + self.arg_cfg)
            return False
        if not os.access(self.arg_dest, os.W_OK):
            self.log.error('No write access to: ' + self.arg_dest)
            return False

        if call([self.cmd, '-t', 'cifs', '-o', 'credentials=' + self.arg_cfg, self.arg_url, self.arg_dest]) == 0:
            return True
        else:
            return False

    @classmethod
    def instance(cls, params):
        cmd = MountSamba()
        if Parameter.CONFIG_FILE in params:
            cmd.arg_cfg = params[Parameter.CONFIG_FILE]
        else:
            raise ParameterError(Parameter.CONFIG_FILE + ' parameter is missing!')
        if Parameter.URL in params:
            cmd.arg_url = params[Parameter.URL]
        else:
            raise ParameterError(Parameter.URL + ' parameter is missing!')
        if Parameter.DEST_DIR in params:
            cmd.arg_dest = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        return cmd

    @classmethod
    def prototype(cls):
        return MountSamba()


class UMount(SystemCommand):
    """Unmounts a mounting point."""

    def __init__(self):
        SystemCommand.__init__(self, 'umount', 'umount')
        self.__arg_dir = ''

    @property
    def arg_dir(self):
        return self.__arg_dir

    @arg_dir.setter
    def arg_dir(self, value):
        self.__arg_dir = value

    def _execute_command(self):
        if not os.access(self.arg_dir, os.W_OK):
            self.log.error('No write access to: ' + self.arg_dir)
            return False

        if call([self.cmd, self.arg_dir]) == 0:
            return True
        else:
            return False

    @classmethod
    def instance(cls, params):
        cmd = UMount()
        if Parameter.DIR in params:
            cmd.arg_dir = params[Parameter.DIR]
        else:
            raise ParameterError(Parameter.DIR + ' parameter is missing!')
        return cmd

    @classmethod
    def prototype(cls):
        return UMount()