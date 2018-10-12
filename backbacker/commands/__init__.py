
# from backbacker.commands.mount import MountSamba
# from backbacker.commands.mount import UMount
# from backbacker.commands.mv_timestamp import MoveTimestamp
# from backbacker.commands.mysql_dump_gzip import MySqlDumpGZip
# from backbacker.commands.pgsql_dump_gzip import PgSqlDumpGZip
# from backbacker.commands.rsync import Rsync
# from backbacker.commands.service import ServiceStart
# from backbacker.commands.service import ServiceStop

__author__ = 'Christof Pieloth'


def command_prototypes():
    """Returns prototypes of all known commands."""
    prototypes = list()
    # prototypes.append(MountSamba.prototype())
    # prototypes.append(MoveTimestamp.prototype())
    # prototypes.append(MySqlDumpGZip.prototype())
    # prototypes.append(PgSqlDumpGZip.prototype())
    # prototypes.append(Rsync.prototype())
    # prototypes.append(ServiceStart.prototype())
    # prototypes.append(ServiceStop.prototype())
    # prototypes.append(UMount.prototype())
    return prototypes


def register_sub_commands(subparser):
    """
    Register backup commands to a subparser.

    :param subparser: A argparse subparser.
    """
    from backbacker.commands.backup_rotation import BackupRotationCliCommand
    from backbacker.commands.compress import GZipCliCommand
    from backbacker.commands.example import ExampleCliCommand
    from backbacker.commands.git import GitBundleCliCommand
    from backbacker.commands.git import GitCloneCliCommand
    from backbacker.commands.github import GithubCloneCliCommand
    from backbacker.commands.mercurial import HgBundleCliCommand

    BackupRotationCliCommand.init_subparser(subparser)
    ExampleCliCommand.init_subparser(subparser)
    GitBundleCliCommand.init_subparser(subparser)
    GitCloneCliCommand.init_subparser(subparser)
    GithubCloneCliCommand.init_subparser(subparser)
    GZipCliCommand.init_subparser(subparser)
    HgBundleCliCommand.init_subparser(subparser)
