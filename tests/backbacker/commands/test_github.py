import os.path
import tempfile
import unittest

import backbacker.commands.github as github

__author__ = 'christof.pieloth'


class GithubBundleTestCase(unittest.TestCase):

    def setUp(self):
        self._dst_dir_tmp = tempfile.TemporaryDirectory(prefix='githubBundleTest')
        self._dst_dir = self._dst_dir_tmp.name

    def tearDown(self):
        self._dst_dir = None
        self._dst_dir_tmp.cleanup()

    def test_execute(self):
        github_clone = github.GithubBundle(username='cpieloth', dst_dir=self._dst_dir)
        github_clone.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'BackBacker.git.bundle')))
