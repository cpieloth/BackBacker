__author__ = 'Christof Pieloth'

import backbacker.commands as cmds
import backbacker.tasks as task


class Job:
    """
    A job is a collection of commands and tasks which are executed sequentially,
    e.g. to backup a web server with all files, database and so on.
    """

    def __init__(self):
        self._commands = []

    def add_command(self, cmd):
        self._commands.append(cmd)

    def execute(self):
        errors = 0
        for cmd in self._commands:
            if not cmd.execute():
                errors += 1
        return errors

    @staticmethod
    def read_job(fname):
        prototypes = []
        # Add commands
        prototypes.append(cmds.compress_gzip.CompressGZip.prototype())
        prototypes.append(cmds.service.ServiceStart.prototype())
        prototypes.append(cmds.service.ServiceStop.prototype())
        # Add tasks
        prototypes.append(task.redmine.Redmine.prototype())

        job_file = open(fname, 'r')

        job = Job()
        for line in job_file:
            for p in prototypes:
                if p.matches(line):
                    # TODO read parameters
                    cmd = p.instance({})
                    job.add_command(cmd)
                    continue

        job_file.close()
        return job
