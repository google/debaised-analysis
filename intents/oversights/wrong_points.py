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
This module detects the wrong point oversight.
Wrong points oversight alerts the user when the sheet contains
wrong points that possibly represent NO data.
Sample case where this oversight will be helpful-
A column has values representing NO data like -99
and then user calculates average of that column.
Ideally the wrong entries should not be considered, but
the results of the intent will be wrong. So, in such cases
the suggestion helps the user in data cleaning.
"""
from util import enums, constants

def wrong_points(table):
    """
    This function detects the case when the table contains wrong points.
    It detects
    1. Entries representing NO data
    2. Some Values being greater than the sum of all the rest of the values
    ToDo(Think about more instances in the list, as also mentioned in the
         schematic description doc - the list is not exhaustive)
    Agrs:
        table: Type pandas.DataFrame
            the initial table in the user's sheets.

    Returns:
        If the oversight is detected, a dictionary containing the
        suggestion is returned.

    """
    # Checking for entries representing NO data
    
    for col in table.columns:

        # Considering only number columns
        if str(table[col].dtype) not in ['float64', 'int64']:
            continue

        extreme_points = [table[col].min(), table[col].max(), -99, 0]

        for extreme_point in extreme_points:

            number_occurrences = 0
            total_values = 0

            # Counting number of occurrences
            for value in table[col]:
                if value == extreme_point:
                    number_occurrences += 1
                total_values += 1

            parameter = number_occurrences / total_values

            if parameter > constants.WRONG_POINTS_THRESHOLD:
                suggestion = {}
                suggestion['oversight'] = enums.Oversights.WRONG_POINTS
                suggestion['suggestion'] = 'Some cells in the table may be wrongly written, maybe to represent NO data'
                suggestion['confidence_score'] = parameter
                return suggestion



    # Detecting entries that may be result of some typing error
    # Like if user mistypes an extra zero in any entry

    for col in table.columns:

        # Considering only +ve number columns
        if str(table[col].dtype) not in ['float64', 'int64'] or table[col].min() < 0:
            continue

        max_entry = table[col].max()
        sum_of_others = table[col].sum() - max_entry

        if max_entry > sum_of_others:
            suggestion = {}
            suggestion['oversight'] = enums.Oversights.WRONG_POINTS
            suggestion['suggestion'] = 'Some of the entry in the table may have been wrongly typed as they excede the sum of other entries'
            return suggestion

