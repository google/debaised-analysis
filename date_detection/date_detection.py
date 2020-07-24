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
This module detects all the date/time containing columns.
Pandas to_datetime function is used to convert string dates to datetime objects.
And then classifies each date column into 3 types-
1. Consistent  - (There is atleast 1 unabiguous date in the column & all
                  unambiguous dates follow same date order)
2. Inconsistent - (Set of unambiguous dates don't follow the same date order)
3. All Ambiguous - (No date is unambiguous)

And if the column type is 'Consistent' then it also
returns date_first = True / False.

date_first = Bool is an extra argument required of parsing ambiguous dates in
pandas.to_datetime function
"""

import re
import datetime
import pandas

# This module will detect all the columns that are date columns
import date_columns_detection

# This module will detect the type(Consistent,all ambiguous,inconsistent column)
# a passed column is & also wether day_first is True/False for that column
import date_column_type_detection

# Function in this module will add the min date & mx date for each column as a key
from util import min_max_date

def detect(table):
    """
    This function first detects the date columns in the table and
    then the date order present in them.

    Args:
        table - Type Pandas dataframe
    Returns:
        A dictionary of date column names as keys and their
        corresponding types date order as values.
    """

    date_columns = date_columns_detection.detect(table)

    # this will return a dict { 'date_column_name' : {type_str, day_first}}
    # type_str = 'Consistent' / 'all ambiguous' / 'inconsistent column'
    # in case of 'Constient' column day_first = True / False
    # in other cases day_first = None

    column_type_and_order = {}

    for column in date_columns:
        column_type_and_order[column] = \
        date_column_type_detection.\
        get_column_type_and_order(table[column].tolist())

    # adding min_date & max_date for each date column to prefill start date &
    # end date in date range aspect in the User Interface

    column_type_and_order = min_max_date.update_min_max_date(column_type_and_order, table)

    return column_type_and_order
