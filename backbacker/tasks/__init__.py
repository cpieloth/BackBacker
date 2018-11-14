__author__ = 'Christof Pieloth'


def register_sub_commands(subparser):
    """
    Register backup commands to a subparser.

    :param subparser: A argparse subparser.
    """
    from backbacker.tasks import redmine

    redmine.RedmineAMCliCommand.init_subparser(subparser)
