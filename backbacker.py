#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
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

    print('Backup started ...')

    # Read config
    args = parser.parse_args()
    if args.config:
        cfg = Config.read_config(args.config)
    else:
        print('No config file specified. Using default settings.')
        cfg = Config()
    cfg.apply_logging()

    # Read job
    job = Job.read_job(args.job)

    # Execute job
    errors = 0
    if job:
        errors += job.execute()
    else:
        print('Could not create job. Backup cancelled!')
        errors += 1

    print('Backup finished with errors: ' + str(errors))
    return errors


if __name__ == '__main__':
    main()
