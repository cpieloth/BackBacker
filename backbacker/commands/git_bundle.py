#!/usr/bin/env python

__author__ = 'Christof Pieloth'

import os
from subprocess import call
from backbacker.commands.command import SystemCommand
from backbacker.constants import Parameter
from backbacker.errors import ParameterError


class GitBundle(SystemCommand):
    """Bundles a git repository."""

    def __init__(self):
        SystemCommand.__init__(self, 'git_bundle', 'git')
        self.__arg_src = ''
        self.__arg_dest = ''

    @property
    def arg_src(self):
        return self.__arg_src

    @arg_src.setter
    def arg_src(self, src):
        self.__arg_src = src

    @property
    def arg_dest(self):
        return self.__arg_dest

    @arg_dest.setter
    def arg_dest(self, dest):
        self.__arg_dest = dest

    def _execute_command(self):
        if not os.access(self.arg_src, os.R_OK):
            self.log.error('No read access to: ' + self.arg_src)
            return False
        if not os.access(self.arg_dest, os.W_OK):
            self.log.error('No write access to: ' + self.arg_dest)
            return False

        os.chdir(self.arg_src)
        dest_file = os.path.basename(self.arg_src) + '.git.bdl'
        dest = os.path.join(self.arg_dest, dest_file)
        if call([self.cmd, 'bundle', 'create', dest, '--all']) == 0:
            return True
        else:
            return False

    @classmethod
    def instance(cls, params):
        cmd = GitBundle()
        if Parameter.SRC_DIR in params:
            cmd.arg_src = params[Parameter.SRC_DIR]
        else:
            raise ParameterError(Parameter.SRC_DIR + ' parameter is missing!')
        if Parameter.DEST_DIR in params:
            cmd.arg_dest = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        return cmd

    @classmethod
    def prototype(cls):
        return GitBundle()