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
        self.__param_src = ''
        self.__param_dest = ''

    @property
    def param_src(self):
        return self.__param_src

    @param_src.setter
    def param_src(self, src):
        self.__param_src = src

    @property
    def param_dest(self):
        return self.__param_dest

    @param_dest.setter
    def param_dest(self, dest):
        self.__param_dest = dest

    def execute(self):
        if not os.access(self.param_src, os.R_OK):
            self.log.error('No read access to: ' + self.param_src)
            return False
        if not os.access(self.param_dest, os.W_OK):
            self.log.error('No write access to: ' + self.param_dest)
            return False

        os.chdir(self.param_src)
        dest_file = os.path.basename(self.param_src) + '.git.bdl'
        dest = os.path.join(self.param_dest, dest_file)
        if call([self.cmd, 'bundle', 'create', dest, '--all']) == 0:
            return True
        else:
            return False

    @classmethod
    def instance(cls, params):
        cmd = GitBundle()
        if Parameter.SRC_DIR in params:
            cmd.param_src = params[Parameter.SRC_DIR]
        else:
            raise ParameterError(Parameter.SRC_DIR + ' parameter is missing!')
        if Parameter.DEST_DIR in params:
            cmd.param_dest = params[Parameter.DEST_DIR]
        else:
            raise ParameterError(Parameter.DEST_DIR + ' parameter is missing!')
        return cmd

    @classmethod
    def prototype(cls):
        return GitBundle()