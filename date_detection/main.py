"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
"""
This module contains the date detection function that gets called by the UI.
It returns a json containing the dict of all the detected date columns.
"""
import date_detection
from util import enums
import pandas, json

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    
    table = request_json
    
    # Converting the list of list into a pandas dataframe.
    query_table = []
    for row in range(1, len(table)):
        if row != 0:
            query_table.append(table[row])
    query_table_dataframe = pandas.DataFrame(query_table,
                                             columns=table[0])

    result = date_detection.detect(query_table_dataframe)


    # converting enums to strings for returning to the UI
    for col in result.keys():
        result[col]['type'] = _column_types_enum_to_str(result[col]['type'])

    result_json = json.dumps(result)

    return result_json

def _column_types_enum_to_str(column_type):
    """This function converts the ColumnTypes eumn to string
    Args:
        column_type- ColumnTypes enum member
    Returns:
        string that represents the column type
    Raises:
        Exception if date column type does not matches
    """
    if column_type == enums.ColumnTypes.CONSISTENT:
        return 'CONSISTENT'
    elif column_type == enums.ColumnTypes.ALL_AMBIGUOUS:
        return 'ALL_AMBIGUOUS'
    elif column_type == enums.ColumnTypes.INCONSISTENT:
        return 'INCONSISTENT'
    else:
        raise Exception("column_type does not match any of the enum members")
