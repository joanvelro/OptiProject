"""
.. module:: test.test_converter
   :synopsis: Unitary test to check the behaviour of the data converter

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
import unittest

from test import get_test_path, REPORTS_PATH

from opti_suite.opti_app.model.engine import Engine
from opti_suite.opti_app.factory.model_data_factory import ModelDataFactory


class ConverterTest(unittest.TestCase):
    """
    ``This class defines the unitary test for the data converter``
    """

    def test_converter(self):
        """
        ``Test converter``
        """
        file_name = 'input_instance.json'
        file_path = get_test_path(filename=file_name)
        data_instance = ModelDataFactory.create_from_json_file(json_request_path=file_path)

        engine = Engine(data_instance)
        engine.execute(verbosity=False, solver='cbc', opt_parameters={'ratioGAP': 0.0001})

        engine.generate_excel_report(filename=REPORTS_PATH + 'input_instance_report.xlsx')
