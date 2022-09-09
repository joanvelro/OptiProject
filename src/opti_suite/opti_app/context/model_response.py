"""
.. module:: opti_suite.opti_app.context.model_response
   :synopsis: This class contains the response of the optimization engine.

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""


class ModelResponse(object):
    """

    `This class defines the ModelResponse data class with the response of the optimization engine.`

            *Attributes*:

                *schedule* :
                ``DataFrame that contains the schedule solution.``

            *Methods*:

                *set_schedule* :
                ``Define the schedule data frame.``

                *get_schedule* :
                ``Return the schedule data frame.``

            """

    def __init__(self) -> None:
        self.__schedule = None

    def set_schedule(self, schedule_df):
        self.__schedule = schedule_df

    # -----------------------------------------

    def get_schedule(self):
        return self.__schedule
