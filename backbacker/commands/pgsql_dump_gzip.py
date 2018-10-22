import logging
import os
import subprocess

from backbacker.command import SystemCommand, CliCommand
from backbacker.constants import Parameter


__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class PgSqlDumpGZip(SystemCommand):
    """Does a PostgreSQL database dump and gzips the output."""

    def __init__(self):
        super().__init__('pg_dump')
        self._dst_dir = ''
        self.db_name = ''
        self.db_user = ''
        self.db_passwd = ''
        self.db_schema = ''
        self.db_table = ''

    @property
    def dst_dir(self):
        return self._dst_dir

    @dst_dir.setter
    def dst_dir(self, value):
        self._dst_dir = os.path.expanduser(value)

    def is_available(self):
        return SystemCommand.check_version(self.cmd)

    def _execute_command(self):
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))
        dest = os.path.join(self.dst_dir, self.db_name + '.sql.gz')

        # auth
        pg_dump = 'PGPASSWORD="' + self.db_passwd + '" pg_dump -U ' + self.db_user
        # schema & table
        if self.db_schema != '':
            pg_dump += ' -n ' + self.db_schema
        if self.db_table != '':
            pg_dump += ' -t ' + self.db_table
        # compression
        pg_dump += ' -Z 9'
        # database and output
        pg_dump += ' ' + self.db_name
        pg_dump += ' > ' + dest
        log.info(pg_dump)

        subprocess.check_call([pg_dump], shell=True)


class PgSqlDumpGzipCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        # TODO(cpieloth): improve help
        subparsers.add_argument('--{}'.format(Parameter.DEST_DIR), help='dest dir', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DB_NAME), help='db name', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DB_USER), help='user', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DB_PASSWD), help='password', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DB_SCHEMA), help='db schema')
        subparsers.add_argument('--{}'.format(Parameter.DB_TABLE), help='db table')

    @classmethod
    def _name(cls):
        return 'pgsqldump'

    @classmethod
    def _help(cls):
        return PgSqlDumpGZip.__doc__

    @classmethod
    def _instance(cls, args):
        instance = PgSqlDumpGZip()
        instance.dst_dir = args[Parameter.DEST_DIR]
        instance.db_name = args[Parameter.DB_NAME]
        instance.db_user = args[Parameter.DB_USER]
        instance.db_passwd = args[Parameter.DB_PASSWD]

        if Parameter.DB_SCHEMA in args:
            instance.db_schema = args[Parameter.DB_SCHEMA]
        if Parameter.DB_TABLE in args:
            instance.db_table = args[Parameter.DB_TABLE]

        return instance
