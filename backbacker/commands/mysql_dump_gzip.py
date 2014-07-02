#!/usr/bin/env python

__author__ = 'Christof Pieloth'

import os
from subprocess import call

from backbacker.commands.command import SystemCommand
from backbacker.constants import Parameter
from backbacker.errors import ParameterError


class MySqlDumpGZip(SystemCommand):
    """Does a MySQL database dump and gzips the output."""

    CMD_GZIP = 'gzip'

    def __init__(self):
        SystemCommand.__init__(self, 'mysqldump_gzip', 'mysqldump')
        self.__arg_dest = ''
        self.__arg_dbname = ''
        self.__arg_dbuser = ''
        self.__arg_dbpasswd = ''

    @property
    def arg_dest(self):
        return self.__arg_dest

    @arg_dest.setter
    def arg_dest(self, value):
        self.__arg_dest = value

    @property
    def arg_dbname(self):
        return self.__arg_dbname

    @arg_dbname.setter
    def arg_dbname(self, value):
        self.__arg_dbname = value

    @property
    def arg_dbuser(self):
        return self.__arg_dbuser

    @arg_dbuser.setter
    def arg_dbuser(self, value):
        self.__arg_dbuser = value

    @property
    def arg_dbpasswd(self):
        return self.__arg_dbpasswd

    @arg_dbpasswd.setter
    def arg_dbpasswd(self, value):
        self.__arg_dbpasswd = value

    def is_available(self):
        success = SystemCommand.check_version(self.cmd)
        success = success and SystemCommand.check_version(MySqlDumpGZip.CMD_GZIP)
        return success

    def _execute_command(self):
        if not os.access(self.arg_dest, os.W_OK):
            self.log.error('No write access to: ' + self.arg_dest)
            return False
        dest = os.path.join(self.arg_dest, self.arg_dbname + '.sql.gz')

        mysqldump = 'mysqldump -u ' + self.arg_dbuser + ' --password=' + self.arg_dbpasswd + ' ' + self.arg_dbname
        gzip = 'gzip > ' + dest

        if call([mysqldump + ' | ' + gzip], shell=True) == 0:
            return True
        else:
            self.log.error('Error while dumping MySQL DB.')
            return False

    @classmethod
    def instance(cls, params):
        cmd = MySqlDumpGZip()
        if Parameter.DEST_DIR in params:
            cmd.arg_dest = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        if Parameter.DB_NAME in params:
            cmd.arg_dbname = params[Parameter.DB_NAME]
        else:
            raise ParameterError(Parameter.DB_NAME + ' parameter is missing!')
        if Parameter.USER in params:
            cmd.arg_dbuser = params[Parameter.USER]
        else:
            raise ParameterError(Parameter.USER + ' parameter is missing!')
        if Parameter.PASSWD in params:
            cmd.arg_dbpasswd = params[Parameter.PASSWD]
        else:
            raise ParameterError(Parameter.PASSWD + ' parameter is missing!')
        return cmd

    @classmethod
    def prototype(cls):
        return MySqlDumpGZip()