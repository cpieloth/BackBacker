__author__ = 'Christof Pieloth'

from backbacker.tasks.redmine import Redmine


def task_prototypes():
    """Returns prototypes of all known tasks."""
    prototypes = [Redmine.prototype()]
    return prototypes