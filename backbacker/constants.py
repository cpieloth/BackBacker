__author__ = 'Christof Pieloth'


class Parameter(object):
    """Parameter for a consistent use in commands, tasks and job file."""
    # Paths and files
    SRC_DIR = 'src_dir'
    DEST_DIR = 'dest_dir'
    DIR = 'dir'
    CONFIG_FILE = 'cfg_file'

    # Network
    URL = 'url'

    # Authentication
    USER = 'user'
    PASSWD = 'passwd'

    # Database
    DB_NAME = 'db_name'

    # Misc
    DATE_FORMAT = 'datefmt'
    ROTATE = 'rotate'


class Constants(object):
    DATE_PREFIX_SEPARATOR = '_'
    KEEP_BACKUPS = 5
    FILE_DATE_FORMAT = '%Y%m%dT%H%M%S'