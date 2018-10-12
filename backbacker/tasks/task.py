import logging

from backbacker.command import Command

__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class Task(Command):
    """A task combines more than one command or task to one unit."""

    def __init__(self):
        super().__init__()

    def _pre_execute(self):
        """Abstract method, is executed before execute_task."""
        return True

    def execute(self):
        """Runs pre_execute, execute_task, post_execute."""
        # FIXME(cpieloth): Check pre_execute, execute_task, post_execute, execute for return code vs exception!
        try:
            success = self._pre_execute()
            if not success:
                return False
            success = success and self._execute_task()
            success = success and self._post_execute()
        except Exception as ex:
            success = False
            log.error('Unexpected error: ' + str(ex))
        return success

    def _execute_task(self):
        """Abstract method, implements the specific functionality."""
        log.error('No yet implemented: ' + str(self.name))
        return False

    def _post_execute(self):
        """Abstract method, is executed after execute_task."""
        return True

    @classmethod
    def instance(cls, params):
        """Abstract method, returns an initialized instance of a specific command."""
        raise Exception('Missing factory method for: ' + str(cls))

    @classmethod
    def prototype(cls):
        """Abstract method, returns an instance of a specific command, e.g. for matches() or is_available()"""
        raise Exception('Prototype method not implemented for: ' + str(cls))
