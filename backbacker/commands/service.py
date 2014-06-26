__author__ = 'Christof Pieloth'

import logging as log
import subprocess

from backbacker.commands.command import SystemCommand


class Service(SystemCommand):
    def __init__(self, name, command):
        SystemCommand.__init__(self, name, 'service')
        self._param_service = ''
        self._param_command = command

    @property
    def param_service(self):
        return self._param_service

    @param_service.setter
    def param_service(self, service):
        self._param_service = service

    @property
    def param_command(self):
        return self._param_command

    def execute(self):
        if not self.param_service:
            log.error('Bad service name: ' + str(self.param_service))
            return False

        if not self.param_command == 'start' and not self.param_command == 'stop':
            log.error('Bad command: ' + str(self.param_command))
            return False

        try:
            subprocess.call([self.cmd, self.param_service, self.param_command], stdout=subprocess.PIPE)
            return True
        except OSError as err:
            log.error('Error on calling \'service ' + self.param_service + ' ' + self.param_command + '\': ' + str(err))
            return False


class ServiceStart(Service):
    """Starts a service using 'service' command."""

    def __init__(self):
        Service.__init__(self, 'service_start', 'start')

    @classmethod
    def instance(cls, params):
        cmd = ServiceStart()
        if 'service' in params:
            cmd.param_service = params['service']
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
            cmd.param_service = params['service']
        return cmd

    @classmethod
    def prototype(cls):
        return ServiceStop()