import io
import sys
import unittest

import backbacker.commands.example

__author__ = 'christof.pieloth'


class ExampleCommandTestCase(unittest.TestCase):

    def test_execute(self):
        cmd = backbacker.commands.example.ExampleCommand('foo')

        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            cmd.execute()
        finally:
            sys.stdout = sys.__stdout__

        self.assertEqual('Hello foo!\n', captured_output.getvalue())
