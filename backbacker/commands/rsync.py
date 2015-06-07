__author__ = 'Christof Pieloth'

import os
from subprocess import call

from backbacker.constants import Parameter
from backbacker.errors import ParameterError

from .command import SystemCommand


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
        super().__init__('rsync', 'rsync')
        self.__arg_src = ''
        self.__arg_dest = ''
        self.__arg_backup_dir = ''
        self.__arg_mirror = False
        self.__arg_rsh = ''

    @property
    def arg_src(self):
        return self.__arg_src

    @arg_src.setter
    def arg_src(self, value):
        self.__arg_src = os.path.expanduser(value)

    @property
    def arg_dest(self):
        return self.__arg_dest

    @arg_dest.setter
    def arg_dest(self, value):
        self.__arg_dest = os.path.expanduser(value)

    @property
    def arg_mirror(self):
        return self.__arg_mirror

    @arg_mirror.setter
    def arg_mirror(self, value):
        self.__arg_mirror = value

    @property
    def arg_backup_dir(self):
        return self.__arg_backup_dir

    @arg_backup_dir.setter
    def arg_backup_dir(self, value):
        self.__arg_backup_dir = os.path.expanduser(value)

    @property
    def arg_rsh(self):
        return self.__arg_rsh

    @arg_rsh.setter
    def arg_rsh(self, value):
        self.__arg_rsh = value

    def execute(self):
        if self.arg_rsh == '':
            if not os.access(self.arg_src, os.R_OK):
                self.log.error('No read access to: ' + self.arg_src)
                return False
            if not os.access(self.arg_dest, os.W_OK):
                self.log.error('No write access to: ' + self.arg_dest)
                return False

        cmd = [self.cmd, Rsync.ALL]
        if self.arg_mirror:
            cmd.append(Rsync.DELETE_DEST)
            if self.arg_backup_dir != '':
                cmd.append(Rsync.BACKUP_DELETE)
                cmd.append(Rsync.BACKUP_DELETE_DIR + self.arg_backup_dir)
        if self.arg_rsh != '':
            cmd.append(Rsync.REMOTE_SHELL + ' ' + self.arg_rsh)
        cmd.append(self.arg_src)
        cmd.append(self.arg_dest)

        if call(cmd) == 0:
            return True
        else:
            return False

    @classmethod
    def instance(cls, params):
        cmd = Rsync()
        if Parameter.SRC_DIR in params:
            cmd.arg_src = params[Parameter.SRC_DIR]
        else:
            raise ParameterError(Parameter.SRC_DIR + ' parameter is missing!')
        if Parameter.DEST_DIR in params:
            cmd.arg_dest = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        if Parameter.MIRROR in params:
            cmd.arg_mirror = True
        if Parameter.BACKUP_DIR in params:
            cmd.arg_backup_dir = params[Parameter.BACKUP_DIR]
        if Parameter.SHELL in params:
            cmd.arg_rsh = params[Parameter.SHELL]
        return cmd

    @classmethod
    def prototype(cls):
        return Rsync()
