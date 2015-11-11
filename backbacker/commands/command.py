__author__ = 'Christof Pieloth'

import argparse
import logging


class Command(object):
    """
    A command is a basic and often an atomic functionality for a backup job, e.g. copying a file.
    """

    def __init__(self):
        self.log = logging.getLogger(self.name())

    @classmethod
    def name(cls):
        """
        Name of the command. Is used to interpret the job script.

        :return Name of the command.
        """
        NotImplementedError('This method must be implemented by each command.')

    @classmethod
    def help(cls):
        """
        Help message or description.

        :return A help message or description.
        """
        NotImplementedError('This method must be implemented by each command.')

    def execute(self):
        """
        Abstract method, implements the specific functionality.

        :return True on success.
        """
        raise NotImplementedError('This method must be implemented by each command.')

    @classmethod
    def init_parser(cls, parser=None):
        """
        Creates an ArgumentParser or adds a sub parser for this command.

        :param parser: ArgumentParser instance or None.
        :return:
        """
        if not parser:
            parser = argparse.ArgumentParser(prog=cls.name())
            parser.description = cls.help()
        else:
            parser = parser.add_parser(cls.name(), help=cls.help())
        cls.register_arguments(parser)
        parser.set_defaults(func=cls.__execute)
        return parser

    @classmethod
    def register_arguments(cls, parser):
        """
        Registers arguments for this command.

        :param parser: Argument parser instance.
        :return: Prepared parser.
        """
        raise NotImplementedError('This method must be implemented by each command.')

    @classmethod
    def instance(cls, arguments=None):
        """
        Creates an instance of the command.

        :param arguments: Namespace with arguments.
        :return: Ready-to-use instance.
        """
        raise NotImplementedError('This method must be implemented by each command.')

    @classmethod
    def __execute(cls, arguments=None):
        """
        Creates an instance and executes the command.

        :param arguments: Namespace with arguments.
        :return: True on success.
        """
        cmd = cls.instance(arguments)
        return cmd.execute()


class SystemCommand(Command):
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
            self.log.error('Not available!')
            return False

        return self._execute_command()

    def _execute_command(self):
        """
        Abstract method, implements the specific functionality.

        :return True on success.
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


class Task(Command):
    """
    A task combines more than one command or task to one unit.
    """

    def __init__(self):
        super().__init__()

    def _pre_execute(self):
        """
        Is executed before execute_task, e.g. to set up environment or check preconditions.

        :return True on success.
        """
        return True

    def execute(self):
        """
        Runs pre_execute, execute_task, post_execute.

        :return True on success.
        """
        try:
            success = self._pre_execute()
            if not success:
                return False
            success = success and self._execute_task()
            success = success and self._post_execute()
        except Exception as ex:
            success = False
            self.log.error('Unexpected error: ' + str(ex))
        return success

    def _execute_task(self):
        """
        Abstract method, implements the specific functionality.

        :return True on success.
        """
        raise NotImplementedError('This method must be implemented by each Task.')

    def _post_execute(self):
        """
        Is executed after execute_task, e.g. to clean up environment.

        :return True on success.
        """
        return True


class ExampleCommand(Command):
    """
    An example how to implement a command.
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    @classmethod
    def name(cls):
        return 'example'

    @classmethod
    def help(cls):
        return 'This is an example command.'

    @classmethod
    def register_arguments(cls, parser):
        parser.add_argument('--value', help='Example value.', required=True)

    @classmethod
    def instance(cls, arguments=None):
        cmd = cls(arguments.value)
        return cmd

    def execute(self):
        print('%s executed: value=%s' % (self.name(), self.value))
        return True


if __name__ == '__main__':
    # Use via CLI or for a job script.
    example_parser = ExampleCommand.init_parser()
    args = example_parser.parse_args()
    args.func(args)

    # Use via API
    example_cmd = ExampleCommand('foo')
    example_cmd.execute()
