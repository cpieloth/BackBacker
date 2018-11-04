import os.path
import tempfile
import unittest

import backbacker.commands.git as git

__author__ = 'christof.pieloth'


class GitCloneTestCase(unittest.TestCase):

    def setUp(self):
        self._dst_dir_tmp = tempfile.TemporaryDirectory(prefix='gitCloneTest')
        self._dst_dir = os.path.join(self._dst_dir_tmp.name, 'cloned')

    def tearDown(self):
        self._dst_dir = None
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
