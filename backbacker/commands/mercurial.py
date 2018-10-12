import logging
import os
import subprocess

from backbacker.command import SystemCommand, CliCommand


__author__ = 'Christof Pieloth'

log = logging.getLogger(__name__)


class HgBundle(SystemCommand):
    """Bundles a hg repository."""

    def __init__(self, repo=None, file=None):
        super().__init__('hg')
        self._repo = repo
        self._dst_dir = file

        # perform checks
        self.repo = self._repo
        self.dst_dir = self._dst_dir

    @property
    def repo(self):
        """Absolute path to repository to bundle."""
        return self._repo

    @repo.setter
    def repo(self, value):
        self._repo = os.path.abspath(os.path.expanduser(value))

    @property
    def dst_dir(self):
        """Absolute path to save the bundle to."""
        return self._dst_dir

    @dst_dir.setter
    def dst_dir(self, value):
        self._dst_dir = os.path.abspath(os.path.expanduser(value))

    @property
    def dst_file(self):
        """
        Generated FQN to bundle file.
        Takes folder name of the repository and add '.git.bundle'
        """
        if not self.repo or not os.path.isdir(self.repo):
            raise NotADirectoryError('repo is None or not a directory: {}'.format(self.repo))
        dst_file = '{}.{}'.format(os.path.basename(self.repo), 'hg.bundle')
        return os.path.join(self.dst_dir, dst_file)

    def _execute_command(self):
        if not os.access(self.repo, os.R_OK):
            raise PermissionError('No read access to: {}'.format(self.repo))
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))

        os.chdir(self.repo)
        subprocess.check_call([self.cmd, 'bundle', '--base', 'null', self.dst_file])


class HgBundleCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, subparsers):
        subparsers.add_argument('-r', '--repo', help='Mercurial repository to bundle.', required=True)
        subparsers.add_argument('-d', '--dst_dir', help='Destination directory to store the bundle.', required=True)

    @classmethod
    def _name(cls):
        return 'hg_bundle'

    @classmethod
    def _help(cls):
        return HgBundle.__doc__

    @classmethod
    def _instance(cls, args):
        return HgBundle(args.repo, args.dst_dir)
