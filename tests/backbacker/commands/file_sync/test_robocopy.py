import os
import shutil
import sys
import tempfile
import unittest
import backbacker.commands.file_sync as file_sync


@unittest.skipUnless(sys.platform.startswith('win'), 'requires Windows')
class RobocopyTestCase(unittest.TestCase):

    def setUp(self):
        self._test_dir_tmp = tempfile.TemporaryDirectory(prefix='robocopyTest')
        self._test_dir = self._test_dir_tmp.name
        self._src_dir = os.path.join(self._test_dir, 'src')
        self._dst_dir = os.path.join(self._test_dir, 'dst')
        self._fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

        shutil.copytree(self._fixtures_dir, self._src_dir)
        os.mkdir(self._dst_dir)

    def tearDown(self):
        self._test_dir_tmp.cleanup()

    def test_mirror_initial(self):
        fs = file_sync.Robocopy()
        fs.src_dir = self._src_dir
        fs.dst_dir = self._dst_dir
        fs.mirror = True
        fs.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'foo', 'foo.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'bar.txt')))
