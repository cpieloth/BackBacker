__author__ = 'Christof Pieloth'

from backbacker.commands.command import SystemCommand


class CompressGZip(SystemCommand):
    """Compresses a folder to a tar.gz archive."""

    def __init__(self):
        SystemCommand.__init__(self, 'tar.gz', 'tar')

    def execute(self):
        # TODO
        print(self.name)
        return True

    @classmethod
    def instance(cls, params):
        return CompressGZip()

    @classmethod
    def prototype(cls):
        return CompressGZip()