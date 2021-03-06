import logging
import os
import subprocess

from backbacker import command


__author__ = 'Christof Pieloth'

logger = logging.getLogger(__name__)


class MySqlDumpGZip(command.SystemCommand):
    """Does a MySQL database dump and gzips the output."""

    CMD_GZIP = 'gzip'

    def __init__(self):
        super().__init__('mysqldump')
        self._dst_dir = ''
        self.db_name = ''
        self.db_user = ''
        self.db_passwd = ''

    @property
    def dst_dir(self):
        return self._dst_dir

    @dst_dir.setter
    def dst_dir(self, value):
        self._dst_dir = os.path.expanduser(value)

    def is_available(self):
        success = super().is_available()
        # TODO(cpieloth): Use command of compress module.
        success = success and command.SystemCommand.check_version(MySqlDumpGZip.CMD_GZIP)
        return success

    def _execute_command(self):
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))
        dest = os.path.join(self.dst_dir, self.db_name + '.sql.gz')

        mysqldump = 'mysqldump -u ' + self.db_user + ' --password=' + self.db_passwd + ' ' + self.db_name
        gzip = 'gzip > ' + dest

        subprocess.check_call([mysqldump + ' | ' + gzip], shell=True)


class MySqlDumpGzipCliCommand(command.CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(command.Argument.DST_DIR.long_arg, required=True, help='Destination directory for dump.')
        parser.add_argument(command.Argument.DB_NAME.long_arg, required=True, help='Database name to dump.')
        parser.add_argument(command.Argument.DB_USER.long_arg, required=True, help='Database user.')
        parser.add_argument(command.Argument.DB_PASSWD.long_arg, required=True, help='Password for database user.')

    @classmethod
    def _name(cls):
        return 'mysqldump'

    @classmethod
    def _help(cls):
        return MySqlDumpGZip.__doc__

    @classmethod
    def _instance(cls, args):
        instance = MySqlDumpGZip()
        instance.dst_dir = command.Argument.DST_DIR.get_value(args)
        instance.db_name = command.Argument.DB_NAME.get_value(args)
        instance.db_user = command.Argument.DB_USER.get_value(args)
        instance.db_passwd = command.Argument.DB_PASSWD.get_value(args)
        return instance
