__author__ = 'Christof Pieloth'

import os
from subprocess import call

from backbacker.commands.command import SystemCommand
from backbacker.errors import ParameterError
from backbacker.constants import Parameter


class CompressGZip(SystemCommand):
    """Compresses a folder to a tar.gz archive."""

    def __init__(self):
        SystemCommand.__init__(self, 'tar.gz', 'tar')
        self.__arg_src = ''
        self.__arg_dest = ''

    @property
    def arg_src(self):
        return self.__arg_src

    @arg_src.setter
    def arg_src(self, src):
        self.__arg_src = src

    @property
    def arg_dest(self):
        return self.__arg_dest

    @arg_dest.setter
    def arg_dest(self, dest):
        self.__arg_dest = dest

    def _execute_command(self):
        if not os.access(self.arg_src, os.R_OK):
            self.log.error('No read access to: ' + self.arg_src)
            return False
        if not os.access(self.arg_dest, os.W_OK):
            self.log.error('No write access to: ' + self.arg_dest)
            return False

        os.chdir(self.arg_src)
        dest_file = os.path.basename(self.arg_src) + '.tar.gz'
        dest = os.path.join(self.arg_dest, dest_file)
        if call([self.cmd, '-zcf', dest, self.arg_src]) == 0:
            return True
        else:
            return False

    @classmethod
    def instance(cls, params):
        cmd = CompressGZip()
        if Parameter.SRC_DIR in params:
            cmd.arg_src = params[Parameter.SRC_DIR]
        else:
            raise ParameterError(Parameter.SRC_DIR + ' parameter is missing!')
        if Parameter.DEST_DIR in params:
            cmd.arg_dest = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        return cmd

    @classmethod
    def prototype(cls):
        return CompressGZip()