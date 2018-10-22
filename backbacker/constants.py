__author__ = 'Christof Pieloth'


class Parameter(object):
    """Parameter for a consistent use in commands, tasks and job file."""
    # Paths and files
    SRC_DIR = 'src_dir'
    DEST_DIR = 'dest_dir'
    DIR = 'dir'
    BACKUP_DIR = 'backup_dir'
    CONFIG_FILE = 'cfg_file'

    # Network
    URL = 'url'

    # Authentication
    USER = 'user'
    PASSWD = 'passwd'

    # Database
    DB_NAME = 'db_name'
    DB_SCHEMA = 'db_schema'
    DB_TABLE = 'db_table'
    DB_USER = 'db_user'
    DB_PASSWD = 'db_passwd'

    # Misc
    DATE_FORMAT = 'datefmt'
    ROTATE = 'rotate'
    MIRROR = 'mirror'
    SHELL = 'shell'


class Constants(object):
    DATE_PREFIX_SEPARATOR = '_'
    KEEP_BACKUPS = 5
    FILE_DATE_FORMAT = '%Y%m%dT%H%M%S'
