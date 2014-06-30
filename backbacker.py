#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import logging
from backbacker.config import Config
from backbacker.job import Job


def main():
    # Prepare CLI arguments
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.name = 'BackBacker'
    parser.description = 'A light backup tool.'
    parser.add_argument("-c", "--config", help="Config file.")
    parser.add_argument("-j", "--job", help="Job file.", required=True)
    parser.epilog = 'BackBacker  Copyright (C) 2014  Christof Pieloth\n' \
                    'This program comes with ABSOLUTELY NO WARRANTY; see LICENSE file.\n' \
                    'This is free software, and you are welcome to redistribute it\n' \
                    'under certain conditions; see LICENSE file.'

    # Read config
    args = parser.parse_args()
    if args.config:
        cfg = Config.read_config(args.config)
    else:
        print('No config file specified. Using default settings.')
        cfg = Config()
    cfg.apply_logging()

    log = logging.getLogger('BackBacker')
    log.info('Backup started ...')

    # Read job
    try:
        job = Job.read_job(args.job)
    except IOError as err:
        log.fatal('Could not read job file: ' + str(err))
        return 1

    # Execute job
    errors = 0
    try:
        errors = job.execute()
    except Exception as ex:
        log.error('Unexpected error during job execution: ' + str(ex))
        errors += 1

    log.info('Backup finished with ' + str(errors) + ' errors.')
    return errors


if __name__ == '__main__':
    main()
