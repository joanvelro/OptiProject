"""
.. module:: opti_suite.opti_app.factory.model_data_factory
   :synopsis: This class processes the input raw data and creates a ModelData which provides access to all the available
   data.
.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
import time
import json
import traceback
import logging
from abc import ABC
from pandas import DataFrame

from opti_suite.opti_app.constants import ColName, SheetName
from opti_suite.opti_app.context.model_data import ModelData
from opti_suite.opti_app.context.exception import OptiSuiteException


logger = logging.getLogger(__name__)


class ModelDataFactory(ABC):
    """

    ``This class processes the input raw data and creates a ModelData which provides access to all the available data.``

                *Attributes*:

                    *data* :
                    ``A ModelData instance.``

                    *request* :
                    ``Input raw data - json file format.``


                *Methods*:

                    *create* :
                    ``Execute the internal methods to generate a ModelData instance from the input request.``

                    *create_from_json_file* :
                    ``Execute the internal methods to generate a ModelData instance from an input json file request.``

                """

    def __init__(self, request) -> None:
        self.request = request
        self.data = ModelData()

    @staticmethod
    def create(request):
        return ModelDataFactory(request).__create()

    @staticmethod
    def create_from_json_file(json_request_path):
        with open(json_request_path, 'r') as file:
            request = json.load(file)

        return ModelDataFactory(request).__create()

    def __create(self):
        try:
            logger.info('Building data model...')
            start = time.time()
            self.__build_configuration()
            self.__build_workers()
            self.__build_periods()
            self.__build_shifts()

            end = time.time()
            logger.info(f'done! It took {round(end - start, 3)} seconds\n')

        except OptiSuiteException:
            raise

        except Exception as err:
            raise OptiSuiteException('Unexpected error building data model') from err

        return self.data

    def __build_configuration(self):
        """
        Build Configuration
        """
        logger.info('\tBuild configuration...')
        configuration_df = self.__read_request_data(sheet_name=SheetName.CONFIGURATION)
        self.data.set_configuration(configuration_df=configuration_df)

    def __build_workers(self):
        """
        Build Workers
        """
        logger.info('\tBuild workers...')
        workers_df = self.__read_request_data(sheet_name=SheetName.WORKERS)
        self.data.set_workers(workers=workers_df)

    def __build_periods(self):
        """
        Build Planning Periods
        """
        logger.info('\tBuild periods...')
        periods_df = self.__read_request_data(sheet_name=SheetName.PERIODS)
        self.data.set_periods(periods=periods_df)

    def __build_shifts(self):
        """
        Build Shifts
        """
        logger.info('\tBuild Shifts...')
        shifts_df = self.__read_request_data(sheet_name=SheetName.SHIFTS)
        shifts_df = shifts_df.set_index(ColName.SHIFT)
        shifts_dict = shifts_df.to_dict()[ColName.PERIOD]
        self.data.set_shifts_ids(shifts_list=list(shifts_dict.keys()))
        self.data.set_shifts(shifts_dict=shifts_dict)

    def __read_request_data(self, sheet_name):
        """
        This method reads the json tag provided and gives as output a dataframe
        """
        try:
            data = DataFrame.from_dict(self.request[sheet_name])

        except (ValueError, KeyError):
            data = None

        except TypeError as err:
            logger.info(f'Unexpected input data format: {err}\n{traceback.format_exc()}')
            raise

        return data
