import logging
import os

from backbacker.commands.compress import GZip
from backbacker.commands.mysql_dump_gzip import MySqlDumpGZip
from backbacker.commands.service import ServiceStart
from backbacker.commands.service import ServiceStop
from backbacker.errors import ParameterError
from backbacker.constants import Parameter

from .task import Task

__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class RedmineAM(Task):
    """Does a backup from Redmine running with Apache2 and MySQL."""

    def __init__(self):
        super().__init__()
        self.__arg_src = ''
        self.__arg_dest = ''
        self.__arg_dbname = ''
        self.__arg_dbuser = ''
        self.__arg_dbpasswd = ''
        self.__cmd_sqldump = MySqlDumpGZip()
        self.__cmd_targz = GZip()

    @property
    def arg_src(self):
        return self.__arg_src

    @arg_src.setter
    def arg_src(self, value):
        self.__arg_src = os.path.expanduser(value)

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

    def _pre_execute(self):
        if not os.access(self.arg_src, os.R_OK):
            log.error('No read access to: ' + self.arg_src)
            return False
        if not os.access(self.arg_dest, os.W_OK):
            log.error('No write access to: ' + self.arg_dest)
            return False

        if not self.__cmd_sqldump.is_available():
            return False

        cmd = ServiceStop()
        cmd.arg_service = 'apache2'
        return cmd.execute()

    def _execute_task(self):
        success = True
        # Compress redmine folder
        self.__cmd_targz.arg_src = self.arg_src
        self.__cmd_targz.arg_dest = self.arg_dest
        success = success and self.__cmd_targz.execute()

        # Dump database
        self.__cmd_sqldump.arg_dest = self.arg_dest
        self.__cmd_sqldump.arg_dbname = self.arg_dbname
        self.__cmd_sqldump.arg_dbuser = self.arg_dbuser
        self.__cmd_sqldump.arg_dbpasswd = self.arg_dbpasswd
        success = success and self.__cmd_sqldump.execute()

        return success

    def _post_execute(self):
        cmd = ServiceStart()
        cmd.arg_service = 'apache2'
        return cmd.execute()

    @classmethod
    def instance(cls, params):
        task = RedmineAM()
        if Parameter.SRC_DIR in params:
            task.arg_src = params[Parameter.SRC_DIR]
        else:
            raise ParameterError(Parameter.SRC_DIR + ' parameter is missing!')
        if Parameter.DEST_DIR in params:
            task.arg_dest = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        if Parameter.DB_NAME in params:
            task.arg_dbname = params[Parameter.DB_NAME]
        else:
            raise ParameterError(Parameter.DB_NAME + ' parameter is missing!')
        if Parameter.USER in params:
            task.arg_dbuser = params[Parameter.USER]
        else:
            raise ParameterError(Parameter.USER + ' parameter is missing!')
        if Parameter.PASSWD in params:
            task.arg_dbpasswd = params[Parameter.PASSWD]
        else:
            raise ParameterError(Parameter.PASSWD + ' parameter is missing!')
        return task

    @classmethod
    def prototype(cls):
        return RedmineAM()
