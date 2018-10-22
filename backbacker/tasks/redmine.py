import logging
import os

from backbacker.command import CliCommand, Argument
from backbacker.commands.compress import GZip
from backbacker.commands.mysql import MySqlDumpGZip
from backbacker.commands.service import ServiceStart
from backbacker.commands.service import ServiceStop

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
        self._cmd_sqldump.dst_dir = self.dst_dir
        self._cmd_sqldump.db_name = self.db_name
        self._cmd_sqldump.db_user = self.db_user
        self._cmd_sqldump.db_passwd = self.db_passwd
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
        subparsers.add_argument(Argument.SRC_DIR.long_arg, help='source dir', required=True)
        subparsers.add_argument(Argument.DST_DIR.long_arg, help='destination dir', required=True)
        subparsers.add_argument(Argument.DB_NAME.long_arg, help='db name', required=True)
        subparsers.add_argument(Argument.DB_USER.long_arg, help='db user', required=True)
        subparsers.add_argument(Argument.DB_PASSWD.long_arg, help='db password', required=True)

    @classmethod
    def _name(cls):
        return 'redmine_am'

    @classmethod
    def _help(cls):
        return RedmineAM.__doc__

    @classmethod
    def _instance(cls, args):
        instance = RedmineAM()
        instance.src_dir = args[Argument.SRC_DIR.key]
        instance.dst_dir = args[Argument.DST_DIR.key]
        instance.db_name = args[Argument.DB_NAME.key]
        instance.db_user = args[Argument.DB_USER.key]
        instance.db_passwd = args[Argument.DB_PASSWD.key]
        return instance

