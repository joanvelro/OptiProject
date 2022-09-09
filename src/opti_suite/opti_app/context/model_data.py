"""
.. module:: opti_suite.opti_app.context.model_data
   :synopsis: This class defines the data class for the input data instance

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""


class ModelData(object):
    """
    ``This class defines the data class ModelData for the optimization library.
    It contains the structures of input data for the optimization problem, loaded from the input request
    as well as the solution data.``

            *Attributes*:

                *workers* :
                ``Dataframe with the input data for unit workers.``

                *periods* :
                ``Dataframe with the input data planning periods.``

                *shifts* :
                ``Dictionary with the time periods for each shift.``

                *shifts_list* :
                ``List of shifts.``

                *configuration* :
                ``Configuration parameters (dataframe).``

                *solution_schedules_worker* :
                ``Dictionary with the schedule solution of workers.``

                *solution_necessary_worker* :
                ``Dictionary with the scheduled workers.``

             *Methods*:

                *set_configuration*

                *set_workers*

                *set_periods*

                *set_shifts*

                *set_shifts_ids*

                *add_solution_scheduled_worker*

                *add_solution_needed_worker*

                *get_configuration*

                *get_config_parameter*

                *get_workers*

                *get_periods*

                *get_shifts*

                *get_shifts_ids*

                *get_solution_scheduled_workers*

                *get_solution_needed_worker*


            """

    def __init__(self) -> None:
        self.__workers = None
        self.__periods = None
        self.__shifts = {}
        self.__shifts_list = []
        self.__configuration = None
        self.__solution_schedules_worker = {}
        self.__solution_necessary_worker = {}

    def set_configuration(self, configuration_df):
        self.__configuration = configuration_df

    def set_workers(self, workers):
        self.__workers = workers

    def set_periods(self, periods):
        self.__periods = periods

    def set_shifts(self, shifts_dict):
        self.__shifts = shifts_dict

    def set_shifts_ids(self, shifts_list):
        self.__shifts_list = shifts_list

    def add_solution_scheduled_worker(self, worker, period, shift, schedule_boolean):
        self.__solution_schedules_worker[worker, period, shift] = schedule_boolean

    def add_solution_needed_worker(self, worker, necessary_boolean):
        self.__solution_necessary_worker[worker] = necessary_boolean
    # ----------------------------------------------------------------------------------------------------------

    def get_config_parameter(self, colname):
        return self.__configuration[colname].values[0]

    def get_workers(self):
        return self.__workers

    def get_periods(self):
        return self.__periods

    def get_shifts(self):
        return self.__shifts

    def get_shifts_ids(self):
        return self.__shifts_list

    def get_solution_scheduled_workers(self):
        return self.__solution_schedules_worker

    def get_solution_needed_worker(self):
        return self.__solution_necessary_worker
