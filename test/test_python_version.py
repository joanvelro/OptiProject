"""
.. module:: test.test_python_version
   :synopsis: Test python version

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
import sys
import unittest


class PythonVersionTest(unittest.TestCase):
    """
    Test python version
    """

    def test_python_version(self):
        """
        Test python version
        """
        python_version = sys.version_info
        self.assertEqual(python_version.major, 3)
        self.assertEqual(python_version.minor, 9)
