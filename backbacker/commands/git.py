import logging
import os
import subprocess

from backbacker.command import SystemCommand, CliCommand, Argument

__author__ = 'Christof Pieloth'

logger = logging.getLogger(__name__)


class GitBundle(SystemCommand):
    """Bundle a git repository."""

    def __init__(self, repo=None, dst_dir=None):
        super().__init__('git')
        self._repo = repo
        self._dst_dir = dst_dir

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
        dst_file = '{}.{}'.format(os.path.basename(self.repo), 'git.bundle')
        return os.path.join(self.dst_dir, dst_file)

    def _execute_command(self):
        if not os.access(self.repo, os.R_OK):
            raise PermissionError('No read access to: {}'.format(self.repo))
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))

        subprocess.check_call([self.cmd, 'bundle', 'create', self.dst_file, '--all'], cwd=self.repo)


class GitBundleCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.SRC_DIR.long_arg, help='git repository to bundle.', required=True)
        parser.add_argument(Argument.DST_DIR.long_arg, help='Destination directory to store the bundle.',
                            required=True)

    @classmethod
    def _help(cls):
        return GitBundle.__doc__

    @classmethod
    def _name(cls):
        return 'git_bundle'

    @classmethod
    def _instance(cls, args):
        return GitBundle(Argument.SRC_DIR.get_value(args), Argument.DST_DIR.get_value(args))


class GitClone(SystemCommand):
    """Clone a git repository."""

    def __init__(self, repo=None, dst_dir=None):
        super().__init__('git')
        self.repo = repo
        self._dst_dir = dst_dir

        # perform checks
        self.dst_dir = self._dst_dir

    @property
    def dst_dir(self):
        """Absolute path to clone the repository to."""
        return self._dst_dir

    @dst_dir.setter
    def dst_dir(self, value):
        self._dst_dir = os.path.abspath(os.path.expanduser(value))

    def _execute_command(self):
        subprocess.check_call([self.cmd, 'clone', self.repo, self.dst_dir])


class GitCloneCliCommand(CliCommand):
    """Clone a git repository."""

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.SRC_DIR.long_arg, help='git repository to clone.', required=True)
        parser.add_argument(Argument.DST_DIR.long_arg, help='Destination directory.', required=True)

    @classmethod
    def _help(cls):
        return GitClone.__doc__

    @classmethod
    def _name(cls):
        return 'git_clone'

    @classmethod
    def _instance(cls, args):
        return GitClone(Argument.SRC_DIR.get_value(args), Argument.DST_DIR.get_value(args))
