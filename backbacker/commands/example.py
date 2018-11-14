from backbacker import command

__author__ = 'Christof Pieloth'


class ExampleCommand(command.Command):
    """An example how to implement a command."""

    def __init__(self, name):
        super().__init__()
        self._name = name

    def execute(self):
        print('Hello {}!'.format(self._name))


class ExampleCliCommand(command.CliCommand):
    """An example how to implement a CLI command for a command."""

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument('--name', help='Name to greet.', required=True)

    @classmethod
    def _name(cls):
        return 'example'

    @classmethod
    def _help(cls):
        return 'Print a welcome message.'

    @classmethod
    def _instance(cls, args):
        return ExampleCommand(args.name)
