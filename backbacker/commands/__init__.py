__author__ = 'Christof Pieloth'


def register_sub_commands(subparser):
    """
    Register backup commands to a subparser.

    :param subparser: A argparse subparser.
    """
    from backbacker.commands import backup_rotation
    from backbacker.commands import compress
    from backbacker.commands import example
    from backbacker.commands import git
    from backbacker.commands import github
    from backbacker.commands import mercurial
    from backbacker.commands import mount
    from backbacker.commands import mv_timestamp
    from backbacker.commands import mysql
    from backbacker.commands import pgsql
    from backbacker.commands import rsync
    from backbacker.commands import service

    backup_rotation.BackupRotationCliCommand.init_subparser(subparser)
    example.ExampleCliCommand.init_subparser(subparser)
    git.GitBundleCliCommand.init_subparser(subparser)
    git.GitCloneCliCommand.init_subparser(subparser)
    github.GithubBundleCliCommand.init_subparser(subparser)
    compress.GZipCliCommand.init_subparser(subparser)
    mercurial.HgBundleCliCommand.init_subparser(subparser)
    mount.MountSambaCliCommand.init_subparser(subparser)
    mount.UmountCliCommand.init_subparser(subparser)
    mv_timestamp.MoveTimestampCliCommand.init_subparser(subparser)
    mysql.MySqlDumpGzipCliCommand.init_subparser(subparser)
    pgsql.PgSqlDumpGzipCliCommand.init_subparser(subparser)
    rsync.RsyncCliCommand.init_subparser(subparser)
    service.ServiceStartCliCommand.init_subparser(subparser)
    service.ServiceStopCliCommand.init_subparser(subparser)
