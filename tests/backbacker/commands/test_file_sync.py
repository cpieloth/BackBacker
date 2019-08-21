import abc
import os
import shutil
import sys
import tempfile
import unittest
import backbacker.commands.file_sync as file_sync


class FileSyncTests(unittest.TestCase, metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def instance(cls):
        raise NotImplementedError()

    def setUp(self):
        self._test_dir_tmp = tempfile.TemporaryDirectory(prefix='rsyncTest')
        self._test_dir = self._test_dir_tmp.name
        self._src_dir = os.path.join(self._test_dir, 'src', '')  # add trailing '/' to have same behaviour like robocopy
        self._dst_dir = os.path.join(self._test_dir, 'dst')
        self._fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures', 'file_sync')

        shutil.copytree(self._fixtures_dir, self._src_dir)
        os.mkdir(self._dst_dir)

    def tearDown(self):
        self._test_dir_tmp.cleanup()

    def test_mirror_initial(self):
        """
        Sync src dir into an empty dst dir.
        All files from src dir must be part of dst dir.
        """
        fs = self.instance()
        fs.src_dir = os.path.join(self._src_dir, '')
        fs.dst_dir = self._dst_dir
        fs.mirror = True
        fs.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'foo', 'foo.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'bar.txt')))

    def test_mirror_initial_exclude_file(self):
        """
        Sync src dir into an empty dst dir excluding a file.
        All files from src dir must be part of dst dir, except the excluded file.
        """
        fs = self.instance()
        fs.src_dir = os.path.join(self._src_dir, '')
        fs.dst_dir = self._dst_dir
        fs.mirror = True
        fs.exclude_files = ['bar.txt']
        fs.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'foo', 'foo.txt')))
        self.assertFalse(os.path.isfile(os.path.join(self._dst_dir, 'bar.txt')))

    def test_mirror_identical(self):
        """
        Sync src dir into identical dst dir.
        All files from src dir must be part of dst dir.
        In Addition: no files should be transferred, but not tested.
        """
        shutil.rmtree(self._dst_dir)
        shutil.copytree(self._fixtures_dir, self._dst_dir)

        fs = self.instance()
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

        fs = self.instance()
        fs.src_dir = self._src_dir
        fs.dst_dir = self._dst_dir
        fs.mirror = True
        fs.execute()

        self.assertTrue(os.path.isfile(os.path.join(self._dst_dir, 'foo', 'foo.txt')))
        self.assertFalse(os.path.isfile(os.path.join(self._dst_dir, 'bar.txt')))


@unittest.skipUnless(sys.platform.startswith('win'), 'requires Windows')
class RobocopyTestCase(FileSyncTests):

    @classmethod
    def instance(cls):
        return file_sync.Robocopy()


@unittest.skipUnless(sys.platform.startswith('linux'), 'requires Linux')
class RsyncTestCase(FileSyncTests):

    @classmethod
    def instance(cls):
        return file_sync.Rsync()


del FileSyncTests  # do not execute base test
