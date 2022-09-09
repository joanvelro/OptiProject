"""
.. module:: test.test_engine
   :synopsis: Unitary test to check the behaviour of the optimization engine

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
import unittest

from test import get_test_path

from opti_suite.opti_app.constants import ResponseKey
from opti_suite.opti_app.model.engine import Engine
from opti_suite.opti_app.factory.model_data_factory import ModelDataFactory


class EngineTest(unittest.TestCase):
    """
    ``This class defines the unitary test for the  scheduler engine``
    """

    def test_engine(self):
        """
        ``Test engine``
        """
        file_name = 'input_instance.json'
        file_path = get_test_path(filename=file_name)
        data_instance = ModelDataFactory.create_from_json_file(json_request_path=file_path)

        engine = Engine(data_instance)
        engine.execute(verbosity=False, solver='cbc', opt_parameters={'ratioGAP': 0.0001})

        json_response = engine.generate_json_response()

        self.assertTrue(isinstance(json_response[ResponseKey.SCHEDULE], list), 'Response incorrect format')
        self.assertTrue(len(json_response[ResponseKey.SCHEDULE]) == 24, 'Response incorrect length')
