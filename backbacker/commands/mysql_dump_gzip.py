import logging
import os
import subprocess

from backbacker.command import SystemCommand, CliCommand
from backbacker.constants import Parameter
from backbacker.errors import ParameterError


__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class MySqlDumpGZip(SystemCommand):
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
        success = SystemCommand.check_version(self.cmd)
        success = success and SystemCommand.check_version(MySqlDumpGZip.CMD_GZIP)
        return success

    def _execute_command(self):
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))
        dest = os.path.join(self.dst_dir, self.db_name + '.sql.gz')

        mysqldump = 'mysqldump -u ' + self.db_user + ' --password=' + self.db_passwd + ' ' + self.db_name
        gzip = 'gzip > ' + dest

        subprocess.check_call([mysqldump + ' | ' + gzip], shell=True)

    @classmethod
    def instance(cls, params):
        cmd = MySqlDumpGZip()
        if Parameter.DEST_DIR in params:
            cmd.dst_dir = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        if Parameter.DB_NAME in params:
            cmd.db_name = params[Parameter.DB_NAME]
        else:
            raise ParameterError(Parameter.DB_NAME + ' parameter is missing!')
        if Parameter.USER in params:
            cmd.db_user = params[Parameter.USER]
        else:
            raise ParameterError(Parameter.USER + ' parameter is missing!')
        if Parameter.PASSWD in params:
            cmd.db_passwd = params[Parameter.PASSWD]
        else:
            raise ParameterError(Parameter.PASSWD + ' parameter is missing!')
        return cmd


class MySqlDumpGzipCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        # TODO(cpieloth): improve help
        subparsers.add_argument('--{}'.format(Parameter.DEST_DIR), help='dest dir', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DB_NAME), help='db name', required=True)
        subparsers.add_argument('--{}'.format(Parameter.USER), help='user', required=True)
        subparsers.add_argument('--{}'.format(Parameter.PASSWD), help='password', required=True)

    @classmethod
    def _name(cls):
        return 'mysqldump'

    @classmethod
    def _help(cls):
        return MySqlDumpGZip.__doc__

    @classmethod
    def _instance(cls, args):
        instance = MySqlDumpGZip()
        instance.dst_dir = args[Parameter.DEST_DIR]
        instance.db_name = args[Parameter.DB_NAME]
        instance.db_user = args[Parameter.USER]
        instance.db_passwd = args[Parameter.PASSWD]
        return instance
