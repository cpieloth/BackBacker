__author__ = 'Christof Pieloth'

from datetime import datetime
import os
from backbacker.commands.command import Command
from backbacker.constants import Constants
from backbacker.constants import Parameter
from backbacker.errors import ParameterError


class MoveTimestamp(Command):
    """Moves/renames all files in a folder to a destination by adding a timestamp prefix."""

    def __init__(self):
        Command.__init__(self, 'mv_timestamp')
        self.__arg_src = ''
        self.__arg_dest = ''
        self.__arg_datefmt = Constants.FILE_DATE_FORMAT

    @property
    def arg_src(self):
        return self.__arg_src

    @arg_src.setter
    def arg_src(self, value):
        self.__arg_src = value

    @property
    def arg_dest(self):
        return self.__arg_dest

    @arg_dest.setter
    def arg_dest(self, value):
        self.__arg_dest = value

    @property
    def arg_datefmt(self):
        return self.__arg_datefmt

    @arg_datefmt.setter
    def arg_datefmt(self, value):
        self.__arg_datefmt = value

    def execute(self):
        if not os.access(self.arg_src, os.R_OK):
            self.log.error('No read access to: ' + self.arg_src)
            return False
        if not os.access(self.arg_dest, os.W_OK):
            self.log.error('No write access to: ' + self.arg_dest)
            return False

        try:
            date_str = datetime.now().strftime(self.arg_datefmt)
        except Exception as ex:
            self.log.error('Could not create date string! Using default format:\n' + str(ex))
            date_str = datetime.now().strftime(Constants.FILE_DATE_FORMAT)

        # Collecting file to avoid conflict if src_dir eq. dest_dir.
        files = []
        for entry in os.listdir(self.arg_src):
            file = os.path.join(self.arg_src, entry)
            if os.path.isfile(file):
                files.append(file)

        errors = 0
        for file_in in files:
            fname = os.path.basename(file_in)
            file_out = os.path.join(self.arg_dest, date_str + Constants.DATE_PREFIX_SEPARATOR + fname)
            try:
                os.rename(file_in, file_out)
            except Exception as ex:
                self.log.error('Could not move file: ' + file_in + '\n' + str(ex))
                errors += 1

        if errors == 0:
            return True
        else:
            return False

    @classmethod
    def instance(cls, params):
        cmd = MoveTimestamp()
        if Parameter.SRC_DIR in params:
            cmd.arg_src = params[Parameter.SRC_DIR]
        else:
            raise ParameterError(Parameter.SRC_DIR + ' parameter is missing!')
        if Parameter.DEST_DIR in params:
            cmd.arg_dest = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        if Parameter.DATE_FORMAT in params:
            cmd.arg_datefmt = params[Parameter.DATE_FORMAT]
        return cmd

    @classmethod
    def prototype(cls):
        return MoveTimestamp()