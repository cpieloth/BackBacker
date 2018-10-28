import logging
import os
import tarfile

from backbacker.command import Command, CliCommand, Argument


__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class GZip(Command):
    """Compresses a folder to a tar.gz archive."""

    def __init__(self):
        super().__init__()
        self._src_dir = None
        self._dst_dir = None

    @property
    def src_dir(self):
        return self._src_dir

    @src_dir.setter
    def src_dir(self, value):
        self._src_dir = os.path.expanduser(value)

    @property
    def dst_dir(self):
        return self._dst_dir

    @dst_dir.setter
    def dst_dir(self, value):
        self._dst_dir = os.path.expanduser(value)

    def execute(self):
        if not os.access(self.src_dir, os.R_OK):
            raise PermissionError('No read access to: {}'.format(self.src_dir))
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))

        dest_file = '{}.tar.gz'.format(os.path.basename(self.src_dir))
        dest = os.path.join(self.dst_dir, dest_file)
        tar = None
        try:
            tar = tarfile.open(dest, 'w|gz')
            tar.add(self.src_dir)
        except Exception as ex:
            raise RuntimeError('Could not compress: {}'.format(self.src_dir)) from ex
        finally:
            if tar:
                tar.close()


class GZipCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.SRC_DIR.long_arg, help='Folder to compress.', required=True)
        parser.add_argument(Argument.DST_DIR.long_arg, required=True,
                            help='Destination directory to store tar.gz.')

    @classmethod
    def _name(cls):
        return 'gzip'

    @classmethod
    def _help(cls):
        return GZip.__doc__

    @classmethod
    def _instance(cls, args):
        instance = GZip()
        instance.src_dir = Argument.SRC_DIR.get_value(args)
        instance.dst_dir = Argument.DST_DIR.get_value(args)
        return instance
