__author__ = 'Christof Pieloth'

from backbacker.commands.command import SystemCommand


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
        # TODO
        print(self.name)
        return True

    @classmethod
    def instance(cls, params):
        cmd = GitBundle()
        if 'src' in params:
            cmd.param_src = params['src']
        if 'dest' in params:
            cmd.param_dest = params['dest']
        return cmd

    @classmethod
    def prototype(cls):
        return GitBundle()