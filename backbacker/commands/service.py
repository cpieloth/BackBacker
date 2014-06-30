__author__ = 'Christof Pieloth'

import subprocess

from backbacker.commands.command import SystemCommand


class Service(SystemCommand):
    def __init__(self, name, command):
        SystemCommand.__init__(self, name, 'service')
        self._arg_service = ''
        self._arg_command = command

    @property
    def arg_service(self):
        return self._arg_service

    @arg_service.setter
    def arg_service(self, service):
        self._arg_service = service

    @property
    def arg_command(self):
        return self._arg_command

    def _execute_command(self):
        if not self.arg_service:
            self.log.error('Bad service name: ' + str(self.arg_service))
            return False

        if not self.arg_command == 'start' and not self.arg_command == 'stop':
            self.log.error('Bad command: ' + str(self.arg_command))
            return False

        try:
            return subprocess.call([self.cmd, self.arg_service, self.arg_command], stdout=subprocess.PIPE) == 0
        except OSError as err:
            self.log.error(
                'Error on calling \'service ' + self.arg_service + ' ' + self.arg_command + '\': ' + str(err))
            return False


class ServiceStart(Service):
    """Starts a service using 'service' command."""

    def __init__(self):
        Service.__init__(self, 'service_start', 'start')

    @classmethod
    def instance(cls, params):
        cmd = ServiceStart()
        if 'service' in params:
            cmd.arg_service = params['service']
        return cmd

    @classmethod
    def prototype(cls):
        return ServiceStart()


class ServiceStop(Service):
    """Stops a service using 'service' command."""

    def __init__(self):
        Service.__init__(self, 'service_stop', 'stop')

    @classmethod
    def instance(cls, params):
        cmd = ServiceStop()
        if 'service' in params:
            cmd.arg_service = params['service']
        return cmd

    @classmethod
    def prototype(cls):
        return ServiceStop()