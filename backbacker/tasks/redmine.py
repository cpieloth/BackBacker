__author__ = 'Christof Pieloth'

from backbacker.tasks.task import Task
from backbacker.commands.service import ServiceStart
from backbacker.commands.service import ServiceStop


class Redmine(Task):
    """Does a backup from Redmine running with Apache2 and MySQL."""

    def __init__(self):
        Task.__init__(self, 'redmine')

    def _pre_execute(self):
        params = {'service': 'apache2'}
        cmd = ServiceStart.instance(params)
        if not cmd.is_available():
            return False
        return cmd.execute()

    def _execute_task(self):
        # TODO compress /var/www/redmine...
        # TODO database dump
        return False

    def _post_execute(self):
        params = {'service': 'apache2'}
        cmd = ServiceStop.instance(params)
        return cmd.execute()

    @classmethod
    def instance(cls, params):
        task = Redmine()
        # TODO set params
        raise task

    @classmethod
    def prototype(cls):
        return Redmine()
