__author__ = 'Christof Pieloth'

import logging

from backbacker.commands import command_prototypes
from backbacker.tasks import task_prototypes
from backbacker.errors import ParameterError


class Job(object):
    """
    A job is a collection of commands and tasks which are executed sequentially,
    e.g. to backup a web server with all files, database and so on.
    """

    log = logging.getLogger(__name__)

    def __init__(self):
        self._commands = []

    def add_command(self, cmd):
        self._commands.append(cmd)

    def execute(self):
        Job.log.info('Starting ...')
        errors = 0
        for cmd in self._commands:
            try:
                if cmd.execute():
                    self.log.info(cmd.name + ' executed.')
                else:
                    errors += 1
                    Job.log.error('Error on executing ' + cmd.name + '!')
            except Exception as ex:
                errors += 1
                Job.log.error('Unknown error:\n' + str(ex))

        Job.log.info('Finished with errors: ' + str(errors))
        return errors

    @staticmethod
    def read_job(fname):
        prototypes = []
        prototypes.extend(command_prototypes())
        prototypes.extend(task_prototypes())

        job_file = None
        job = None
        try:
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
                            Job.log.error("Command '" + p.name + "' is skipped: " + str(err))
                        continue
        except IOError as err:
            job.log.critical('Error on reading job file:\n' + str(err))
            job = None
        except Exception as ex:
            Job.log.critical('Unknown error: \n' + str(ex))
            job = None
        finally:
            if job_file:
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