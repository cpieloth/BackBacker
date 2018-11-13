import logging
import os
import subprocess

from backbacker.command import SystemCommand, CliCommand, Argument


__author__ = 'Christof Pieloth'

logger = logging.getLogger(__name__)


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
        logger.info(pg_dump)

        subprocess.check_call([pg_dump], shell=True)


class PgSqlDumpGzipCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.DST_DIR.long_arg, help='Destination directory for dump for dump.', required=True)
        parser.add_argument(Argument.DB_NAME.long_arg, help='Database name.', required=True)
        parser.add_argument(Argument.DB_USER.long_arg, help='Database user.', required=True)
        parser.add_argument(Argument.DB_PASSWD.long_arg, help='Password for database user.', required=True)
        parser.add_argument(Argument.DB_SCHEMA.long_arg, help='Database schema.')
        parser.add_argument(Argument.DB_TABLE.long_arg, help='Database table.')

    @classmethod
    def _name(cls):
        return 'pgsqldump'

    @classmethod
    def _help(cls):
        return PgSqlDumpGZip.__doc__

    @classmethod
    def _instance(cls, args):
        instance = PgSqlDumpGZip()
        instance.dst_dir = Argument.DST_DIR.get_value(args)
        instance.db_name = Argument.DB_NAME.get_value(args)
        instance.db_user = Argument.DB_USER.get_value(args)
        instance.db_passwd = Argument.DB_PASSWD.get_value(args)

        if Argument.DB_SCHEMA.has_value(args):
            instance.db_schema = Argument.DB_SCHEMA.get_value(args)
        if Argument.DB_TABLE.has_value(args):
            instance.db_table = Argument.DB_TABLE.get_value(args)

        return instance
