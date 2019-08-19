import os
import shutil
import sys
import tempfile
import unittest
import backbacker.commands.file_sync as file_sync


@unittest.skipUnless(sys.platform.startswith('linux'), 'requires Linux')
class RsyncTestCase(unittest.TestCase):

    def setUp(self):
        self._test_dir_tmp = tempfile.TemporaryDirectory(prefix='rsyncTest')
        self._test_dir = self._test_dir_tmp.name
        self._src_dir = os.path.join(self._test_dir, 'src', '')  # add trailing '/' to have same behaviour like robocopy
        self._dst_dir = os.path.join(self._test_dir, 'dst')
        self._fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

        shutil.copytree(self._fixtures_dir, self._src_dir)
        os.mkdir(self._dst_dir)

    def tearDown(self):
        self._test_dir_tmp.cleanup()

    def test_mirror_initial(self):
        """
        Sync src dir into an empty dst dir.
        All files from src dir must be part of dst dir.
        """
        fs = file_sync.Rsync()
        fs.src_dir = os.path.join(self._src_dir, '')
        fs.dst_dir = self._dst_dir
        fs.mirror = True
        fs.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'foo', 'foo.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'bar.txt')))

    def test_mirror_identical(self):
        """
        Sync src dir into identical dst dir.
        All files from src dir must be part of dst dir.
        In Addition: no files should be transferred, but not tested.
        """
        shutil.rmtree(self._dst_dir)
        shutil.copytree(self._fixtures_dir, self._dst_dir)

        fs = file_sync.Rsync()
        fs.src_dir = self._src_dir
        fs.dst_dir = self._dst_dir
        fs.mirror = True
        fs.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'foo', 'foo.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'bar.txt')))

    def test_mirror_removed(self):
        """
        src dir and dst dir are identical, but bar.txt is removed in src dir.
        After sync it must be removed in dst dir, too.
        """
        shutil.rmtree(self._dst_dir)
        shutil.copytree(self._fixtures_dir, self._dst_dir)
        os.remove(os.path.join(self._src_dir, 'bar.txt'))

        fs = file_sync.Rsync()
        fs.src_dir = self._src_dir
        fs.dst_dir = self._dst_dir
        fs.mirror = True
        fs.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'foo', 'foo.txt')))
        self.assertFalse(os.path.isfile(os.path.join(self._dst_dir, 'bar.txt')))
