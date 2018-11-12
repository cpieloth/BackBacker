import os
import shutil
import stat
import tempfile
import unittest

import backbacker.commands.git as git

__author__ = 'christof.pieloth'


class GitCloneTestCase(unittest.TestCase):

    def setUp(self):
        self._dst_dir_tmp = tempfile.TemporaryDirectory(prefix='gitCloneTest')
        self._dst_dir = self._dst_dir_tmp.name

    def tearDown(self):
        shutil.rmtree(os.path.join(self._dst_dir, '.git'), onerror=_on_rm_error)
        self._dst_dir_tmp.cleanup()

    def test_execute_folder(self):
        repo = os.path.abspath(os.path.join(__file__, '..', '..', '..', '..'))

        git_clone = git.GitClone(repo=repo, dst_dir=self._dst_dir)
        git_clone.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'setup.py')))

    def test_execute_url(self):
        repo = 'https://github.com/cpieloth/BackBacker.git'

        git_clone = git.GitClone(repo=repo, dst_dir=self._dst_dir)
        git_clone.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'setup.py')))


class GitBundleTestCase(unittest.TestCase):

    def setUp(self):
        self._dst_dir_tmp = tempfile.TemporaryDirectory(prefix='gitBundleTest')
        self._dst_dir = self._dst_dir_tmp.name

    def tearDown(self):
        self._dst_dir = None
        self._dst_dir_tmp.cleanup()

    def test_execute_folder(self):
        repo = os.path.abspath(os.path.join(__file__, '..', '..', '..', '..'))

        git_bundle = git.GitBundle(repo=repo, dst_dir=self._dst_dir)
        git_bundle.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, git_bundle.dst_file)))


def _on_rm_error(func, path, exc_info):
    # workaround for 'PermissionError: [WinError 5]' on windows
    if isinstance(exc_info[1], PermissionError):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
    else:
        raise exc_info[1]
