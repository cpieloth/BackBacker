import logging
import os
import tempfile
import urllib.parse

import requests

from backbacker.command import Command, CliCommand, Argument
from backbacker.commands.git import GitClone, GitBundle

__author__ = 'christof'

log = logging.getLogger(__name__)


class GithubBundle(Command):
    """Bundle all git repositories from a Github account."""

    def __init__(self, username=None, dst_dir=None):
        self.username = username
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

    def execute(self):
        if not os.access(self.dst_dir, os.W_OK):
            raise PermissionError('No write access to: {}'.format(self.dst_dir))

        for name, url in self.collect_repository_urls(self.username):
            self.clone_and_bundle(name, url)

    @classmethod
    def collect_repository_urls(cls, username):
        # https://developer.github.com/v3/repos/#list-user-repositories
        request_url = 'https://api.github.com/users/{}/repos'.format(urllib.parse.quote(username))

        while request_url:
            response = requests.get(request_url)
            if not response.ok:
                raise IOError('Unsuccessful request: '.format(request_url))

            for repo_dict in response.json():
                yield (repo_dict['name'], repo_dict['git_url'])

            if 'next' in response.links:
                request_url = response.links['next']['url']
            else:
                break
        else:  # no-break
            # https://developer.github.com/v3/#pagination
            log.error('Link header contains empty next URL.')

    def clone_and_bundle(self, name, url):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dst_dir = os.path.join(tmp_dir, name)
            git_clone = GitClone(url, dst_dir)
            git_clone.execute()

            git_bundle = GitBundle(dst_dir, self.dst_dir)
            git_bundle.execute()


class GithubBundleCliCommand(CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(Argument.USER.long_arg, help='Username of the Github account.', required=True)
        parser.add_argument(Argument.DST_DIR.long_arg, help='Destination directory.', required=True)

    @classmethod
    def _help(cls):
        return GithubBundle.__doc__

    @classmethod
    def _name(cls):
        return 'github_clone'

    @classmethod
    def _instance(cls, args):
        return GithubBundle(Argument.USER.get_value(args), Argument.DST_DIR.get_value(args))
