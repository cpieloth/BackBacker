__author__ = 'Christof Pieloth'

import logging as log
import subprocess


class Command:
    """A command is a basic and often an atomic functionality for a backup job, e.g. copying a file."""

    def __init__(self, name):
        self._name = name.lower()
        pass

    @property
    def name(self):
        """Name of the command. Is used to interpret the job script."""
        return self._name

    def execute(self):
        """Abstract method, implements the specific functionality."""
        log.debug('No yet implemented: ' + str(self.name))
        return False

    @classmethod
    def instance(cls, params):
        """Abstract method, returns an initialized instance of a specific command."""
        raise Exception('Instance method not implemented for: ' + str(cls))

    @classmethod
    def prototype(cls):
        """Abstract method, returns an instance of a specific command, e.g. for matches() or is_available()"""
        raise Exception('Prototype method not implemented for: ' + str(cls))

    def matches(self, cmd):
        """Checks if this command should be used for execution."""
        return cmd.lower().startswith(self.name)


class SystemCommand(Command):
    """A system command is a OS-dependent command."""

    def __init__(self, name, cmd=''):
        Command.__init__(self, name)
        self._cmd = cmd

    @property
    def cmd(self):
        return self._cmd

    def is_available(self):
        """Checks if this command is available on the system, uses argument --version."""
        return SystemCommand.check_version(self.cmd)

    @staticmethod
    def check_version(cmd):
        """Checks if  'cmd --version' is callable."""
        try:
            subprocess.call([cmd, '--version'], stdout=subprocess.PIPE)
            return True
        except OSError as err:
            log.error('Error on calling ' + cmd + ': ' + str(err))
            return False