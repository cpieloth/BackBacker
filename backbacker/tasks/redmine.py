import logging
import os

from backbacker.command import CliCommand
from backbacker.commands.compress import GZip
from backbacker.commands.mysql_dump_gzip import MySqlDumpGZip
from backbacker.commands.service import ServiceStart
from backbacker.commands.service import ServiceStop
from backbacker.constants import Parameter

from .task import Task

__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class RedmineAM(Task):
    """Does a backup from Redmine running with Apache2 and MySQL."""

    def __init__(self):
        super().__init__()
        self._src_dir = None
        self._dst_dir = None
        self.db_name = None
        self.db_user = None
        self.db_passwd = None
        self._cmd_sqldump = MySqlDumpGZip()
        self._cmd_targz = GZip()

    @property
    def src_dir(self):
        return self._src_dir

    @src_dir.setter
    def src_dir(self, value):
        self._src_dir = os.path.expanduser(value)

    @property
    def dst_dir(self):
        return self._dst_dir

    @dst_dir.setter
    def dst_dir(self, value):
        self._dst_dir = os.path.expanduser(value)

    def _pre_execute(self):
        if not os.access(self.src_dir, os.R_OK):
            log.error('No read access to: ' + self.src_dir)
            return False
        if not os.access(self.dst_dir, os.W_OK):
            log.error('No write access to: ' + self.dst_dir)
            return False

        if not self._cmd_sqldump.is_available():
            return False

        cmd = ServiceStop()
        cmd.service = 'apache2'
        return cmd.execute()

    def _execute_task(self):
        # FIXME(cpieloth): Check pre_execute, execute_task, post_execute for return code vs exception!

        success = True
        # Compress redmine folder
        self._cmd_targz.src_dir = self.src_dir
        self._cmd_targz.dst_dir = self.dst_dir
        success = success and self._cmd_targz.execute()

        # Dump database
        self._cmd_sqldump.arg_dest = self.dst_dir
        self._cmd_sqldump.arg_dbname = self.db_name
        self._cmd_sqldump.arg_dbuser = self.db_user
        self._cmd_sqldump.arg_dbpasswd = self.db_passwd
        success = success and self._cmd_sqldump.execute()

        return success

    def _post_execute(self):
        cmd = ServiceStart()
        cmd.service = 'apache2'
        return cmd.execute()


class RedmineAMCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        # TODO(cpieloth): improve help
        subparsers.add_argument('--{}'.format(Parameter.SRC_DIR), help='source dir', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DEST_DIR), help='destination dir', required=True)
        subparsers.add_argument('--{}'.format(Parameter.DB_NAME), help='db name', required=True)
        subparsers.add_argument('--{}'.format(Parameter.USER), help='user', required=True)
        subparsers.add_argument('--{}'.format(Parameter.PASSWD), help='password', required=True)

    @classmethod
    def _name(cls):
        return 'redmine_am'

    @classmethod
    def _help(cls):
        return RedmineAM.__doc__

    @classmethod
    def _instance(cls, args):
        instance = RedmineAM()
        instance.src_dir = args[Parameter.SRC_DIR]
        instance.dst_dir = args[Parameter.DEST_DIR]
        instance.db_name = args[Parameter.DB_NAME]
        instance.db_user = args[Parameter.USER]
        instance.db_passwd = args[Parameter.PASSWD]
        return instance

