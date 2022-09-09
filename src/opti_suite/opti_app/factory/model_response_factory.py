"""
.. module:: opti_suite.opti_app.factory.model_response_factory
   :synopsis: Class to build the response of the optimization library

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
import traceback
import logging

from pandas import DataFrame
from abc import ABC

from opti_suite.opti_app.context.model_response import ModelResponse
from opti_suite.opti_app.context.model_data import ModelData
from opti_suite.opti_app.constants import ResponseKey, ColName


logger = logging.getLogger(__name__)


class ModelResponseFactory(ABC):
    """

    ``This class processes the solution raw data and creates the Response instance (engine response).``

            *Attributes*:

                *data* :
                ``The ModelData instance that contains the solution data.``

                *response* :
                ``The response of the optimization engine.``

            *Methods*:

                *create* :
                ``Execute the private methods to build the solution.``


            """

    def __init__(self, data: ModelData) -> None:
        self.response = ModelResponse()
        self.data = data

    @staticmethod
    def create(data):
        """
        Method to create an instance of ModelResponse based on the solution stored in ModelData
        """
        return ModelResponseFactory(data).__create()

    def __create(self):
        try:
            self.__build_schedule()

        except Exception as err:
            logger.exception(f'Error building response: {err}\n{traceback.format_exc()}')
            self.response = None
            raise
        return self.response

    def __build_schedule(self):
        """
        Build Schedule
        """
        scheduled_workers = self.data.get_solution_scheduled_workers()

        workers = []
        periods = []
        shifts = []
        schedules = []

        for ((worker, period, shift), value) in scheduled_workers.items():
            workers.append(worker)
            periods.append(period)
            shifts.append(shift)
            schedules.append(value)

        # Build dataframe
        scheduled_workers_df = DataFrame({
            ResponseKey.SCHEDULE: schedules,
            ColName.WORKER: workers,
            ColName.PERIOD: periods,
            ColName.SHIFT: shifts,
        })

        self.response.set_schedule(schedule_df=scheduled_workers_df)
