import logging
import subprocess

from backbacker.command import SystemCommand, CliCommand


__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class Service(SystemCommand):
    def __init__(self, command):
        super().__init__('service')
        self.service = ''
        self._command = command

    @property
    def command(self):
        return self._command

    def _execute_command(self):
        if not self.service:
            raise ValueError('Empty service name.')

        if not self.command == 'start' and not self.command == 'stop':
            raise ValueError('Bad command: {}'.format(self.command))

        subprocess.check_call([self.cmd, self.service, self.command], stdout=subprocess.PIPE)


class ServiceStart(Service):
    """Starts a service using 'service' command."""

    def __init__(self):
        Service.__init__(self, 'start')


class ServiceStop(Service):
    """Stops a service using 'service' command."""

    def __init__(self):
        Service.__init__(self, 'stop')


class ServiceStartCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        # TODO(cpieloth): improve help
        subparsers.add_argument('--service', help='service', required=True)

    @classmethod
    def _name(cls):
        return 'service_start'

    @classmethod
    def _help(cls):
        return ServiceStart.__doc__

    @classmethod
    def _instance(cls, args):
        instance = ServiceStart()
        instance.service = args.service
        return instance


class ServiceStopCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        # TODO(cpieloth): improve help
        subparsers.add_argument('--service', help='service', required=True)

    @classmethod
    def _name(cls):
        return 'service_stop'

    @classmethod
    def _help(cls):
        return ServiceStop.__doc__

    @classmethod
    def _instance(cls, args):
        instance = ServiceStop()
        instance.service = args.service
        return instance
