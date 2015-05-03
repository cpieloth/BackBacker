__author__ = 'Christof Pieloth'

from .compress import GZip
from .git_bundle import GitBundle
from .hg_bundle import HgBundle
from .mount import MountSamba
from .mount import UMount
from .mv_timestamp import MoveTimestamp
from .mysql_dump_gzip import MySqlDumpGZip
from .pgsql_dump_gzip import PgSqlDumpGZip
from .rsync import Rsync
from .service import ServiceStart
from .service import ServiceStop
from .backup_rotation import BackupRotation


def command_prototypes():
    """Returns prototypes of all known commands."""
    prototypes = []
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
