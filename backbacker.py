#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import logging as log
from backbacker.job import Job


def main():
    # Prepare CLI arguments
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.name = 'BackBacker'
    parser.description = 'A light backup tool.'
    parser.add_argument("-c", "--config", help="Config file.")
    parser.add_argument("-j", "--job", help="Job file.")
    parser.epilog = 'BackBacker  Copyright (C) 2014  Christof Pieloth\n' \
                    'This program comes with ABSOLUTELY NO WARRANTY; see LICENSE file.\n' \
                    'This is free software, and you are welcome to redistribute it\n' \
                    'under certain conditions; see LICENSE file.'

    # Collect CLI arguments
    cfg_file = ''
    bb_file = ''

    args = parser.parse_args()
    if args.config:
        cfg_file = args.config
    if args.job:
        bb_file = args.job

    log.info('Backup started ...')
    # TODO read config file

    try:
        job = Job.read_job(bb_file)
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
