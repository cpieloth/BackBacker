"""Module for CLI command implementations."""

import abc
import logging
import sys

__author__ = 'christof.pieloth'

logger = logging.getLogger(__name__)


def init_logging(cfg):
    """Initializes the logging."""
    from backbacker import config
    if not cfg:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    elif cfg.log_type == config.Config.ARG_LOG_TYPE_CONSOLE:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=cfg.log_format,
                            datefmt=cfg.log_datefmt)
    elif cfg.log_type == config.Config.ARG_LOG_TYPE_FILE:
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
    def _add_arguments(cls, parser):
        """
        Initialize the argument parser and help for the specific sub-command.

        Must be implemented by a sub-command.

        :param parser: A subparser.
        :type parser: argparse.ArgumentParser
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
        parser = subparsers.add_parser(cls._name().strip(), help=cls._help().strip())
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


class BatchCmd(SubCommand):
    """A batch is a collection of commands and tasks which are executed sequentially."""

    @classmethod
    def _name(cls):
        return 'batch'

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument('-c', '--config', help='Config file.')
        parser.add_argument('-i', '--ignore_errors', help='Continue on error.', action='store_true')
        parser.add_argument('batch_file', help='Batch file.')
        return parser

    @classmethod
    def exec(cls, args):
        """Execute the command."""
        from backbacker import backbacker

        init_logging(args.config)

        commands = cls.read_batch_file(args.batch_file)
        error_count = 0
        for command in commands:
            argv = ['nop']
            argv.extend(command.split(' '))
            rc = backbacker.main(argv)

            if rc > 0:
                error_count += 1
                logger.error('Error executing command: %s. Returned with: %d', command, rc)
                if args.ignore_errors:
                    continue
                else:
                    return rc

        return error_count

    @staticmethod
    def read_batch_file(fname):
        commands = list()
        with open(fname, 'r') as file:
            for line in file:
                if line[0] == '#':
                    continue

                commands.append(line.strip())

        return commands


def register_sub_commands(subparser):
    BatchCmd.init_subparser(subparser)
