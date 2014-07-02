__author__ = 'Christof Pieloth'

from .compress_gzip import CompressGZip
from .mv_timestamp import MoveTimestamp
from .mysql_dump_gzip import MySqlDumpGZip
from .git_bundle import GitBundle
from .service import ServiceStart
from .service import ServiceStop


def command_prototypes():
    """Returns prototypes of all known commands."""
    prototypes = []
    prototypes.append(CompressGZip.prototype())
    prototypes.append(GitBundle.prototype())
    prototypes.append(MoveTimestamp.prototype())
    prototypes.append(MySqlDumpGZip.prototype())
    prototypes.append(ServiceStart.prototype())
    prototypes.append(ServiceStop.prototype())
    return prototypes