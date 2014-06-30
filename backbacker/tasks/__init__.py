__author__ = 'Christof Pieloth'

from backbacker.tasks.redmine import RedmineAM


def task_prototypes():
    """Returns prototypes of all known tasks."""
    prototypes = [RedmineAM.prototype()]
    return prototypes