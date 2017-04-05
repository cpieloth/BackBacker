from backbacker.commands.compress import GZip
from backbacker.commands.git_bundle import GitBundle
from backbacker.commands.hg_bundle import HgBundle
from backbacker.commands.mount import MountSamba
from backbacker.commands.mount import UMount
from backbacker.commands.mv_timestamp import MoveTimestamp
from backbacker.commands.mysql_dump_gzip import MySqlDumpGZip
from backbacker.commands.pgsql_dump_gzip import PgSqlDumpGZip
from backbacker.commands.rsync import Rsync
from backbacker.commands.service import ServiceStart
from backbacker.commands.service import ServiceStop
from backbacker.commands.backup_rotation import BackupRotation

__author__ = 'Christof Pieloth'


def command_prototypes():
    """Returns prototypes of all known commands."""
    prototypes = list()
    prototypes.append(GZip.prototype())
    prototypes.append(GitBundle.prototype())
    prototypes.append(HgBundle.prototype())
    prototypes.append(MountSamba.prototype())
    prototypes.append(MoveTimestamp.prototype())
    prototypes.append(MySqlDumpGZip.prototype())
    prototypes.append(PgSqlDumpGZip.prototype())
    prototypes.append(Rsync.prototype())
    prototypes.append(ServiceStart.prototype())
    prototypes.append(ServiceStop.prototype())
    prototypes.append(UMount.prototype())
    prototypes.append(BackupRotation.prototype())
    return prototypes
