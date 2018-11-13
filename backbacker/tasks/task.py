import abc
import logging

from backbacker.command import Command

__author__ = 'Christof Pieloth'

logger = logging.getLogger(__name__)


class Task(Command, metaclass=abc.ABCMeta):
    """A task combines more than one command or task to one unit."""

    def __init__(self):
        super().__init__()

    def _pre_execute(self):
        """
        Optional method, is executed before execute_task.

        :raise Exception on any error.
        """
        pass

    def execute(self):
        """Runs pre_execute, execute_task, post_execute."""
        self._pre_execute()
        self._execute_task()
        self._post_execute()

    @abc.abstractmethod
    def _execute_task(self):
        """
        Abstract method, implements the specific functionality.

        :raise Exception on any error.
        """
        raise NotImplementedError()

    def _post_execute(self):
        """
        Optional method, is executed after execute_task.

        :raise Exception on any error.
        """
        pass
