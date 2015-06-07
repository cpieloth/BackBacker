import argparse
from argparse import RawTextHelpFormatter

from .config import Config
from .job import Job


__version__ = "0.1.0"


def main():
    # Prepare CLI arguments
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
    parser.add_argument("-j", "--job", help="Job file.", required=True)

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
