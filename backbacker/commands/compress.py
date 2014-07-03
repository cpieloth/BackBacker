__author__ = 'Christof Pieloth'

import os
import tarfile

from backbacker.commands.command import Command
from backbacker.errors import ParameterError
from backbacker.constants import Parameter


class GZip(Command):
    """Compresses a folder to a tar.gz archive."""

    def __init__(self):
        Command.__init__(self, 'gzip')
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

    def execute(self):
        if not os.access(self.arg_src, os.R_OK):
            self.log.error('No read access to: ' + self.arg_src)
            return False
        if not os.access(self.arg_dest, os.W_OK):
            self.log.error('No write access to: ' + self.arg_dest)
            return False

        dest_file = os.path.basename(self.arg_src) + '.tar.gz'
        dest = os.path.join(self.arg_dest, dest_file)
        tar = None
        success = True
        try:
            tar = tarfile.open(dest, 'w|gz')
            tar.add(self.arg_src)
        except Exception as ex:
            self.log.error('Could not compress: ' + self.arg_src + '\n' + str(ex))
            success = False
        finally:
            if tar:
                tar.close()

        return success

    @classmethod
    def instance(cls, params):
        cmd = GZip()
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
        return GZip()