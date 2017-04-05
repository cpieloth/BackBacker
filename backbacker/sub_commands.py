"""Module for CLI command implementations."""

import abc
import logging
import sys

from backbacker.config import Config
from backbacker.job import Job

__author__ = 'christof.pieloth'

log = logging.getLogger(__name__)


def init_logging(cfg):
        """Initializes the logging."""
        if not cfg:
            logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        elif cfg.log_type == Config.ARG_LOG_TYPE_CONSOLE:
            logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=cfg.log_format,
                                datefmt=cfg.log_datefmt)
        elif cfg.log_type == Config.ARG_LOG_TYPE_FILE:
            logging.basicConfig(level=logging.DEBUG, filename=cfg.log_file, format=cfg.log_format,
                                datefmt=cfg.log_datefmt)


class SubCommand(abc.ABC):
    """
    Abstract base class for sub commands.

    A new sub command can be added by calling the init_subparser().
    """

    @classmethod
    @abc.abstractmethod
    def _name(cls):
        """
        Return name of the command.

        :return: Command name
        :rtype: str
        """
        raise NotImplementedError()

    @classmethod
    def _help(cls):
        """
        Return help description.

        :return: Help description
        :rtype: str
        """
        return cls.__doc__

    @classmethod
    @abc.abstractmethod
    def _add_arguments(cls, subparsers):
        """
        Initialize the argument parser and help for the specific sub-command.

        Must be implemented by a sub-command.

        :param subparsers: A subparser.
        :type subparsers: argparse.ArgumentParser
        :return: void
        """
        raise NotImplementedError()

    @classmethod
    def init_subparser(cls, subparsers):
        """
        Initialize the argument parser and help for the specific sub-command.

        :param subparsers: A subparser.
        :type subparsers: argparse.ArgumentParser
        :return: void
        """
        parser = subparsers.add_parser(cls._name(), help=cls._help())
        cls._add_arguments(parser)
        parser.set_defaults(func=cls.exec)

    @classmethod
    @abc.abstractmethod
    def exec(cls, args):
        """
        Execute the command.

        Must be implemented by a sub-command.

        :param args: argparse arguments.
        :return: 0 on success.
        """
        raise NotImplementedError()


class JobCmd(SubCommand):
    """Run all commands of a job file."""

    @classmethod
    def _name(cls):
        return 'job'

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument("-c", "--config", help="Config file.")
        parser.add_argument("job_file", help="Job file.")
        return parser

    @classmethod
    def exec(cls, args):
        """Execute the command."""
        init_logging(args.config)

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
