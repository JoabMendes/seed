# coding=utf-8
import unittest

from seed.utilities import run_command
from seed.exceptions import ShellCommandError


class TestRunCommand(unittest.TestCase):

    def setUp(self):
        self.success_command = 'python -c \"print(\'hello world\')\"'
        self.failure_command = 'python -c \"print(\'failed\'); exit(1)\"'

    def test_success(self):
        captured = run_command(self.success_command)
        self.assertEqual(captured, "hello world")

    def testShouldRaiseShellCommandErrorWhenCommandFails(self):
        with self.assertRaises(ShellCommandError):
            run_command(self.failure_command)
