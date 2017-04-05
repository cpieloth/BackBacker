from backbacker.command import Command, CliCommand

__author__ = 'Christof Pieloth'


class ExampleCommand(Command):
    """An example how to implement a command."""

    def __init__(self, name):
        super().__init__()
        self._name = name

    def execute(self):
        print('Hello {}!'.format(self._name))


class ExampleCliCommand(CliCommand):
    """An example how to implement a CLI command for a command."""

    @classmethod
    def _add_arguments(cls, subparsers):
        subparsers.add_argument('--name', help='Name to greet.', required=True)

    @classmethod
    def _name(cls):
        return 'example'

    @classmethod
    def _help(cls):
        return 'Print a welcome message.'

    @classmethod
    def _instance(cls, args):
        return ExampleCommand(args.name)
