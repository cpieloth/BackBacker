__author__ = 'Christof Pieloth'

import logging as log

import backbacker.commands as cmds
import backbacker.tasks as task
from backbacker.errors import ParameterError


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
        prototypes.append(cmds.git_bundle.GitBundle.prototype())
        prototypes.append(cmds.service.ServiceStart.prototype())
        prototypes.append(cmds.service.ServiceStop.prototype())
        # Add tasks
        prototypes.append(task.redmine.Redmine.prototype())

        job_file = open(fname, 'r')

        job = Job()
        for line in job_file:
            if line[0] == '#':
                continue
            for p in prototypes:
                if p.matches(line):
                    params = Job.read_parameter(line)
                    try:
                        cmd = p.instance(params)
                        job.add_command(cmd)
                    except ParameterError as err:
                        log.error("Command '" + p.name + "' is skipped: " + str(err))
                    continue

        job_file.close()
        return job

    @staticmethod
    def read_parameter(line):
        params = {}
        i = line.find(': ') + 2
        line = line[i:]
        pairs = line.split(';')
        for pair in pairs:
            pair = pair.strip()
            par = pair.split('=')
            if len(par) == 2:
                params[par[0]] = par[1]
        return params