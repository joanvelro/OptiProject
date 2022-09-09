"""
.. module:: opti_suite.opti_app.factory.data_converter
   :synopsis: Data Converter

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
import json
import io

from pandas import ExcelWriter, ExcelFile, DataFrame

from opti_suite.opti_app.constants import ResponseKey, SheetName
from opti_suite.opti_app.context.model_response import ModelResponse
from opti_suite.opti_app.context.model_data import ModelData


class DataConverter(object):
    """
    ``This class defines the Data Converter Class that translate the response data model``

            *Attributes*:

                *output_path* :
                ``Output path``

                *input_path* :
                ``Input path``
            """

    def __init__(self, input_path, output_path) -> None:
        self.output_path = output_path
        self.input_path = input_path

    @staticmethod
    def scheduling_response_to_json(response: ModelResponse, output_path=None):
        return DataConverter(input_path=None, output_path=output_path).__scheduling_response_to_json(response)

    @staticmethod
    def scheduling_response_to_excel(response: ModelResponse, data: ModelData = None,
                                     with_request=False, output_path=None):

        return DataConverter(input_path=None, output_path=output_path). \
            __scheduling_response_to_excel(response, data, with_request)

    def __scheduling_response_to_json(self, response: ModelResponse):
        # Data Conversion from SchedulingResponse to json file format
        json_data = dict()

        # Scheduling response config
        scheduling_response_config = {
            ResponseKey.SCHEDULE: response.get_schedule(),
        }

        # Transform every dataframe in response to json
        for (response_key, dataframe) in scheduling_response_config.items():
            if dataframe is not None and not dataframe.empty:
                json_data[response_key] = json.loads(dataframe.to_json(orient='records', indent=2))

        # save json complete
        if self.output_path is not None:
            with open(self.output_path, 'w') as fp:
                json.dump(json_data, fp, indent=2)
        else:
            return json_data

    def __scheduling_response_to_excel(self, response: ModelResponse, data: ModelData = None,
                                       with_request: bool = False):
        input_prefix = 'Input_'

        # Store dataframes in a dict, where the key is the sheet name
        request_frames = dict() if not with_request or data is None else \
            {input_prefix + SheetName.WORKERS: DataFrame(data.get_workers()),
             input_prefix + SheetName.PERIODS: DataFrame(data.get_periods()),
             input_prefix + SheetName.SHIFTS: DataFrame(data.get_shifts_ids()),
             }

        # Store dataframes in a dict, where the key is the sheet name
        response_frames = {ResponseKey.SCHEDULE: response.get_schedule(),
                           }

        # Compose required frames dict
        required_frames = {**request_frames, **response_frames}

        # Initialize the Excel writer
        effective_output = self.output_path if self.output_path is not None else io.BytesIO()
        writer = ExcelWriter(effective_output, engine='xlsxwriter')

        for sheet, frame in required_frames.items():
            if frame is not None:
                frame.to_excel(writer, sheet_name=sheet, index=False)

        writer.save()

        writer.close()

        return ExcelFile(effective_output) if self.output_path is None else None
