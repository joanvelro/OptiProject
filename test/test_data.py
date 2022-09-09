"""
.. module:: test.test_data
   :synopsis: Unitary tests for data used in testing

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
import logging
import unittest

from test import get_test_path
from pandas import DataFrame

from opti_suite.opti_app.factory.model_data_factory import ModelDataFactory

logger = logging.getLogger(__name__)


class DataTest(unittest.TestCase):
    """
    *Data Test*

    This class defines the unitary test for the input data instances that are used in test_engine
    """

    def test_data(self):
        """
        *Test Data Input dummy from json file*
        """
        file_name = 'input_instance.json'

        file_path = get_test_path(filename=file_name)
        model_data_instance = ModelDataFactory.create_from_json_file(json_request_path=file_path)

        self.assertTrue(isinstance(model_data_instance.get_workers(), DataFrame),
                        '(!) Incorrect data structure for workers')
        self.assertTrue(isinstance(model_data_instance.get_periods(), DataFrame),
                        '(!) Incorrect data structure for periods')
        self.assertTrue(isinstance(model_data_instance.get_shifts(), dict),
                        '(!) Incorrect data structure for shifts')

        self.assertTrue(model_data_instance.get_workers().shape[0] == 3, '(!) Incorrect no. of workers')
        self.assertTrue(model_data_instance.get_periods().shape[0] == 5, '(!) Incorrect no. of periods')
        self.assertTrue(len(model_data_instance.get_shifts().keys()) == 2, '(!) Incorrect no. of shifts')
