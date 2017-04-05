"""Entry point for CLI usage."""

import argparse
import sys

import backbacker.sub_commands


def main(argv=sys.argv):
    """
    Start the Example tool.

    :return: 0 on success.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.prog = argv[0]
    parser.name = 'BackBacker'
    parser.description = 'BackBacker is a light backup tool ' \
        'with a "declarative" job file based on simple commands with arguments.'
    parser.epilog = 'BackBacker  Copyright (C) 2015  Christof Pieloth\n' \
                    'This program comes with ABSOLUTELY NO WARRANTY; see LICENSE file.\n' \
                    'This is free software, and you are welcome to redistribute it\n' \
                    'under certain conditions; see LICENSE file.'
    parser.add_argument('--version', action='version', version='BackBacker ' + backbacker.__version__)

    subparser = parser.add_subparsers(title='BackBacker Commands', description='Valid example commands.')
    backbacker.sub_commands.JobCmd.init_subparser(subparser)

    args = parser.parse_args(argv[1:])
    try:
        # Check if a sub-command is given, otherwise print help.
        getattr(args, 'func')
    except AttributeError:
        parser.print_help()
        return 2

    return args.func(args)
