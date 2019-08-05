import os
import unittest

import backbacker.config

__author__ = 'christof.pieloth'


class ConfigTestCase(unittest.TestCase):

    def test_singleton(self):
        cfg1 = backbacker.config.Config()
        cfg2 = backbacker.config.Config()
        self.assertIs(cfg1, cfg2)

        expected_format = 'FOO'
        cfg1.log.format = expected_format
        self.assertEqual(cfg2.log.format, expected_format)

    def test_parse(self):
        cfg = backbacker.config.Config.read_config(os.path.join(os.path.dirname(__file__), 'fixtures', 'config.ini'))
        self.assertEqual(cfg.log.file, '/tmp/backbacker.log')
        self.assertEqual(cfg.log.type, 'console')
