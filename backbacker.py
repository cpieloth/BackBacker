#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import logging as log
import sys
from backbacker.job import Job


def main():
    log.basicConfig(level=log.DEBUG, stream=sys.stdout)

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

    # Collect CLI arguments
    args = parser.parse_args()
    if not args.config:
        log.warn('No config file specified. using default settings.')

    log.info('Backup started ...')
    # TODO read config file

    try:
        job = Job.read_job(args.job)
    except IOError as err:
        log.fatal('Could not read job file: ' + str(err))
        return 1

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
