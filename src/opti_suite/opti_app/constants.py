"""
.. module:: opti_suite.opti_app.constants
   :synopsis: Constants

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
from enum import Enum, unique

ENGINE = 'openpyxl'


class StringEnum(str, Enum):
    """
    ``This class is the base string enumerate.``
    """

    def __str__(self):
        return self.value

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


@unique
class ResponseKey(StringEnum):
    """

    ``This enumerates contains all the scheduling response elements (keys).``
    """
    SCHEDULE = 'Schedule'
    OPTIMAL = 'Optimal'
    FEASIBLE = 'Feasible'
    INFEASIBLE = 'Infeasible'
    INCONSISTENT = 'Inconsistent'


@unique
class SheetName(StringEnum):
    """

    ``This enumerates contains all the sheet names (request keys).``
    """
    WORKERS = 'Workers'
    PERIODS = 'Periods'
    SHIFTS = 'Shifts'
    CONFIGURATION = 'Configuration'


@unique
class ColName(StringEnum):
    """

    ``This enumerates contains all the column names (request and response) and temporal column names of DataFrames.``
    """
    WORKER = 'Worker'
    PERIOD = 'Period'
    SHIFT = 'Shift'
    NAME = 'Name'
    HOURS_PER_SHIFT = 'Hours Per Shift'
    DAILY_HOURS_LIMIT = 'Daily Hours Limit'
    WORK_LOAD = 'Work Load'
    DATE = 'Date'
    PROJECT_NAME = 'Project Name'
    UNITARY_COST = 'Unitary Cost'
