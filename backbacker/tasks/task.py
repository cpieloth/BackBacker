__author__ = 'Christof Pieloth'

import logging


# TODO subclass from command
class Task:
    """A task combines more than one command or task to one unit."""

    def __init__(self, name):
        self._name = name
        self._log = logging.getLogger(self._name)

    @property
    def name(self):
        """Name of the command. Is used to interpret the job script."""
        return self._name

    @property
    def log(self):
        """Logger for this task."""
        return self._log

    def _pre_execute(self):
        """Abstract method, is executed before execute_task."""
        return True

    def execute(self):
        """Runs pre_execute, execute_task, post_execute."""
        try:
            success = self._pre_execute()
            if success:
                success = success or self._execute_task()
            success = success or self._post_execute()
        except Exception as ex:
            success = False
            self.log.error('Unexpected error: ' + str(ex))
        return success

    def _execute_task(self):
        """Abstract method, implements the specific functionality."""
        self.log.error('No yet implemented: ' + str(self.name))
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

    def matches(self, cmd):
        """Checks if this command should be used for execution."""
        return cmd.lower().startswith(self.name)