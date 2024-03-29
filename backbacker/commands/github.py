import logging
import os
import shutil
import stat
import tempfile
import urllib.parse

from backbacker import command
from backbacker.commands import git

__author__ = 'christof'

logger = logging.getLogger(__name__)


class GithubBundle(command.Command):
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
        import requests

        # https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28
        request_url = 'https://api.github.com/users/{}/repos'.format(urllib.parse.quote(username))

        # https://docs.github.com/en/rest/about-the-rest-api/api-versions?apiVersion=2022-11-2
        request_headers = {'X-GitHub-Api-Version': '2022-11-28'}

        while request_url:
            response = requests.get(request_url, headers=request_headers)
            if not response.ok:
                raise IOError('Unsuccessful request: {}, {}'.format(request_url, response.text))

            for repo_dict in response.json():
                yield repo_dict['name'], repo_dict['clone_url']

            # https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api?apiVersion=2022-11-2
            if 'next' in response.links:
                request_url = response.links['next']['url']
            else:
                break
        else:  # no-break
            logger.error('Link header contains empty next URL.')

    def clone_and_bundle(self, name, url):
        with tempfile.TemporaryDirectory(prefix='githubBundle') as tmp_dir:
            dst_dir = os.path.join(tmp_dir, name)
            try:
                git_clone = git.GitClone(url, dst_dir)
                git_clone.execute()

                git_bundle = git.GitBundle(dst_dir, self.dst_dir)
                git_bundle.execute()
            finally:
                shutil.rmtree(dst_dir, onerror=_on_rm_error)


class GithubBundleCliCommand(command.CliCommand):

    @classmethod
    def _add_arguments(cls, parser):
        parser.add_argument(command.Argument.USER.long_arg, help='Username of the Github account.', required=True)
        parser.add_argument(command.Argument.DST_DIR.long_arg, help='Destination directory.', required=True)

    @classmethod
    def _help(cls):
        return GithubBundle.__doc__

    @classmethod
    def _name(cls):
        return 'github_clone'

    @classmethod
    def _instance(cls, args):
        return GithubBundle(command.Argument.USER.get_value(args), command.Argument.DST_DIR.get_value(args))


def _on_rm_error(_, path, exc_info):
    # workaround for 'PermissionError: [WinError 5]' on windows
    if isinstance(exc_info[1], PermissionError):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
    else:
        raise exc_info[1]
