from backbacker.tasks.redmine import RedmineAM

__author__ = 'Christof Pieloth'


def task_prototypes():
    """Returns prototypes of all known tasks."""
    prototypes = [RedmineAM.prototype()]
    return prototypes
