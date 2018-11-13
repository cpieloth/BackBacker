import logging
import os

from backbacker.command import CliCommand, Argument, Task
from backbacker.commands.compress import GZip
from backbacker.commands.mysql import MySqlDumpGZip
from backbacker.commands.service import ServiceStart
from backbacker.commands.service import ServiceStop


__author__ = 'Christof Pieloth'

logger = logging.getLogger(__name__)


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
            raise PermissionError('No read access to: {}'.format(self.src_dir))
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))

        if not self._cmd_sqldump.is_available():
            raise OSError('Command not available: {}'.format(self._cmd_sqldump.cmd))

        cmd = ServiceStop()
        cmd.service = 'apache2'
        cmd.execute()

    def _execute_task(self):
        # Compress redmine folder
        self._cmd_targz.src_dir = self.src_dir
        self._cmd_targz.dst_dir = self.dst_dir
        self._cmd_targz.execute()

        # Dump database
        self._cmd_sqldump.dst_dir = self.dst_dir
        self._cmd_sqldump.db_name = self.db_name
        self._cmd_sqldump.db_user = self.db_user
        self._cmd_sqldump.db_passwd = self.db_passwd
        self._cmd_sqldump.execute()

    def _post_execute(self):
        cmd = ServiceStart()
        cmd.service = 'apache2'
        cmd.execute()


class RedmineAMCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.SRC_DIR.long_arg, help='Redmine folder.', required=True)
        parser.add_argument(Argument.DST_DIR.long_arg, help='Destination director for backup.', required=True)
        parser.add_argument(Argument.DB_NAME.long_arg, help='Database name for Redmine.', required=True)
        parser.add_argument(Argument.DB_USER.long_arg, help='Database user.', required=True)
        parser.add_argument(Argument.DB_PASSWD.long_arg, help='Password for database user.', required=True)

    @classmethod
    def _name(cls):
        return 'redmine_am'

    @classmethod
    def _help(cls):
        return RedmineAM.__doc__

    @classmethod
    def _instance(cls, args):
        instance = RedmineAM()
        instance.src_dir = Argument.SRC_DIR.get_value(args)
        instance.dst_dir = Argument.DST_DIR.get_value(args)
        instance.db_name = Argument.DB_NAME.get_value(args)
        instance.db_user = Argument.DB_USER.get_value(args)
        instance.db_passwd = Argument.DB_PASSWD.get_value(args)
        return instance
