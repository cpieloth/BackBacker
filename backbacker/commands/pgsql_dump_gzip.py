__author__ = 'Christof Pieloth'

import os
from subprocess import call

from backbacker.commands.command import SystemCommand
from backbacker.constants import Parameter
from backbacker.errors import ParameterError


class PgSqlDumpGZip(SystemCommand):
    """Does a PostgreSQL database dump and gzips the output."""

    def __init__(self):
        SystemCommand.__init__(self, 'pgsqldump_gzip', 'pg_dump')
        self.__arg_dest = ''
        self.__arg_dbname = ''
        self.__arg_dbuser = ''
        self.__arg_dbpasswd = ''
        self.__arg_dbschema = ''
        self.__arg_dbtable = ''

    @property
    def arg_dest(self):
        return self.__arg_dest

    @arg_dest.setter
    def arg_dest(self, value):
        self.__arg_dest = os.path.expanduser(value)

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

    @property
    def arg_dbschema(self):
        return self.__arg_dbschema

    @arg_dbschema.setter
    def arg_dbschema(self, value):
        self.__arg_dbschema = value

    @property
    def arg_dbtable(self):
        return self.__arg_dbtable

    @arg_dbtable.setter
    def arg_dbtable(self, value):
        self.__arg_dbtable = value

    def is_available(self):
        return SystemCommand.check_version(self.cmd)

    def _execute_command(self):
        if not os.access(self.arg_dest, os.W_OK):
            self.log.error('No write access to: ' + self.arg_dest)
            return False
        dest = os.path.join(self.arg_dest, self.arg_dbname + '.sql.gz')

        # auth
        pg_dump = 'PGPASSWORD="' + self.arg_dbpasswd + '" pg_dump -U ' + self.arg_dbuser
        # schema & table
        if self.arg_dbschema != '':
            pg_dump += ' -n ' + self.arg_dbschema
        if self.arg_dbtable != '':
            pg_dump += ' -t ' + self.arg_dbtable
        # compression
        pg_dump += ' -Z 9'
        # database and output
        pg_dump += ' ' + self.arg_dbname
        pg_dump += ' > ' + dest
        self.log.info(pg_dump)

        if call([pg_dump], shell=True) == 0:
            return True
        else:
            self.log.error('Error while dumping PostgreSQL DB.')
            return False

    @classmethod
    def instance(cls, params):
        cmd = PgSqlDumpGZip()
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
        if Parameter.DB_SCHEMA in params:
            cmd.arg_dbschema = params[Parameter.DB_SCHEMA]
        if Parameter.DB_TABLE in params:
            cmd.arg_dbtable = params[Parameter.DB_TABLE]
        return cmd

    @classmethod
    def prototype(cls):
        return PgSqlDumpGZip()
