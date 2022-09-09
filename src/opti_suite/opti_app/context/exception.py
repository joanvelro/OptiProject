"""
.. module:: opti_suite.opti_app.context.exception
   :synopsis: Exception

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""


class OptiSuiteException(Exception):
    """
    ``OptiSuite runtime exception.``
    """
    def __init__(self, message):  # real signature unknown
        super().__init__(message)


class OptiSuiteDataException(Exception):
    """
    ``OptiSuite Data exception.``
    """
    def __init__(self, message, errors_dict):  # real signature unknown
        super().__init__(message)
        self.messages = errors_dict

    def get_scheduling_messages(self):
        return self.messages
