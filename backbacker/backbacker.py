"""Entry point for CLI usage."""

import argparse
import sys


def main(argv=sys.argv):
    """
    Start the Example tool.

    :return: 0 on success.
    """
    from backbacker import __version__
    from backbacker.sub_commands import register_sub_commands as register_base_commands
    from backbacker.commands import register_sub_commands as register_backup_command

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.prog = argv[0]
    parser.name = 'BackBacker'
    parser.description = 'BackBacker is a light backup tool ' \
        'with a "declarative" job file based on simple commands with arguments.'
    parser.epilog = 'BackBacker  Copyright (C) 2015  Christof Pieloth\n' \
                    'This program comes with ABSOLUTELY NO WARRANTY; see LICENSE file.\n' \
                    'This is free software, and you are welcome to redistribute it\n' \
                    'under certain conditions; see LICENSE file.'
    parser.add_argument('--version', action='version', version='BackBacker ' + __version__)

    subparser = parser.add_subparsers(title='BackBacker Commands', description='Valid example commands.')
    register_base_commands(subparser)
    register_backup_command(subparser)

    args = parser.parse_args(argv[1:])
    try:
        # Check if a sub-command is given, otherwise print help.
        getattr(args, 'func')
    except AttributeError:
        parser.print_help()
        return 2

    return args.func(args)
