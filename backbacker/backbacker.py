import argparse
from argparse import RawTextHelpFormatter
import logging
import sys

from .config import Config
from .job import Job


__version__ = "0.1.0"


def init_logging(cfg):
        """Initializes the logging."""
        if cfg.log_type == Config.ARG_LOG_TYPE_CONSOLE:
            logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=cfg.log_format,
                                datefmt=cfg.log_datefmt)
        elif cfg.log_type == Config.ARG_LOG_TYPE_FILE:
            logging.basicConfig(level=logging.DEBUG, filename=cfg.log_file, format=cfg.log_format,
                                datefmt=cfg.log_datefmt)


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.prog = 'backbacker'
    parser.name = 'BackBacker'
    parser.description = 'BackBacker is a light backup tool ' \
        'with a "declarative" job file based on simple commands with arguments.'
    parser.epilog = 'BackBacker  Copyright (C) 2014  Christof Pieloth\n' \
                    'This program comes with ABSOLUTELY NO WARRANTY; see LICENSE file.\n' \
                    'This is free software, and you are welcome to redistribute it\n' \
                    'under certain conditions; see LICENSE file.'

    parser.add_argument('--version', action='version', version='BackBacker ' + __version__)
    parser.add_argument("-c", "--config", help="Config file.")
    parser.add_argument("job_file", help="Job file.")

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Read config
    if args.config:
        cfg = Config.read_config(args.config)
    else:
        print('No config file specified. Using default settings.')
        cfg = Config()

    # Init logging
    init_logging(cfg)
    log = logging.getLogger('BackBacker')

    # Read job
    job = Job.read_job(args.job_file)
    if not job:
        log.critical('Could not create job. Backup cancelled!')
        return 1

    # Execute job
    log.info('Start backup ...')
    errors = job.execute()
    if errors == 0:
        log.info('Backup successfully finished.')
    else:
        log.error('Backup finished with %i errors!' % errors)

    return errors
