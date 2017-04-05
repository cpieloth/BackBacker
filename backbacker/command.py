"""
A command is the core component of BackBacker.
A concrete command implements the back-up logic.
"""

import abc
import logging
from backbacker.sub_commands import SubCommand

__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class Command(abc.ABC):
    """
    A command is a basic and often an atomic functionality for a backup job, e.g. copying a file.
    Implementations can be used for API access.
    """

    @abc.abstractmethod
    def execute(self):
        """
        Abstract method, implements the specific functionality.

        :raise Exception on error
        """
        raise NotImplementedError()


class SystemCommand(Command, metaclass=abc.ABCMeta):
    """
    A system command is a OS-dependent command. It checks the availability before execution.
    """

    def __init__(self, cmd):
        super().__init__()
        self._cmd = cmd

    @property
    def cmd(self):
        return self._cmd

    def is_available(self):
        """Checks if this command is available on the system, uses argument --version."""
        return SystemCommand.check_version(self.cmd)

    def execute(self):
        if not self.is_available():
            log.error('Not available!')
            raise OSError('Command not available: {}'.format(self.cmd))

        self._execute_command()

    @abc.abstractmethod
    def _execute_command(self):
        """
        Abstract method, implements the specific functionality.

        :raise Exception on error
        """
        raise NotImplementedError('This method must be implemented by each SystemCommand.')

    @staticmethod
    def check_version(cmd):
        """
        Checks if  'cmd --version' is callable.

        :return True 'cmd --version' has return code 0.
        """
        import subprocess
        try:
            return subprocess.call([cmd, '--version'], stdout=subprocess.PIPE) == 0
        except OSError:
            return False


class Task(Command, metaclass=abc.ABCMeta):
    """
    A task combines more than one command or task to one unit.
    """

    def __init__(self):
        super().__init__()

    def _pre_execute(self):
        """
        Is executed before execute_task, e.g. to set up environment or check preconditions.

        :raise Exception on error
        """
        pass

    def execute(self):
        self._pre_execute()
        self._execute_task()
        self._post_execute()

    @abc.abstractmethod
    def _execute_task(self):
        """
        Abstract method, implements the specific functionality.

        :raise Exception on error
        """
        raise NotImplementedError()

    def _post_execute(self):
        """
        Is executed after execute_task, e.g. to clean up environment.

        :raise Exception on error
        """
        pass


class CliCommand(SubCommand, metaclass=abc.ABCMeta):
    """Wraps a Command to a CLI sub-command."""

    @classmethod
    @abc.abstractmethod
    def _instance(cls, args):
        """
        Creates an instance of the command.

        :param args: argparse arguments.
        :return: A ready-to-use Command instance.
        :rtype: backbacker.commands.Command
        """
        raise NotImplementedError()

    @classmethod
    def exec(cls, args):
        instance = cls._instance(args)
        try:
            instance.execute()
            return 0
        except Exception as ex:
            log.error(ex)
            return 1
