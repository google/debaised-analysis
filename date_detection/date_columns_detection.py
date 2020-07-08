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
This module will detect all the columns that are date columns.
The hurestic used -
A column will be classified as a datetime column 
if it has a 'date'/'year'/'time'/'month'/'time' keyword in it
& all dates are parseable by the pandas.to_datetime function
or if it follows one of the standard datetime formats listed
below. 
Note - we may at modify the hurestic at a later point of time
       when we encounter some cases that are not handled correctly
"""
import re
import datetime
import pandas

def detect(table):
    """
    This function iterates over each column in the table &
    lists each column that is classified as a datetime column
    using a hurestic.

    Args :
        table : Type-pandas dataframe
                the table that is used to detect 
    """
    # initialized the possible date columns to all the columns.
    date_columns = []

    # for each column in the table if it has 'date' as a substring or
    # it follows any 6 of the date formats we consider it as a date column.
    for column in table.columns:
        # passing only the column instead of entire table is efficient
        column_as_list = table[column].tolist()
        if _possible_date_column(column_as_list, column):
            date_columns.append(column)

    return date_columns

def _possible_date_column(column, column_name):
    """
    This module checkes if the passed column is a date/time column using the
    Hurestic : Keywords like 'date', 'year' etc. are present as a substring
               in column name. Also these columns should be parseable with
               to_datetime method of pandas. If no keyword is present -
               check if it matches some standard formats.
    Args:
        column - Type list
            It contains the entries of the column passed
        column_name - Type Str
            It is the name of the column passed.
    Returns:
        Type - Bool
            True if the column contains dates/times
    """
    # Convert integers in the list to strings
    column = [str(entry) for entry in column]

    # regular expression . substitute replaces all chars other that a-z & A-Z
    # in column_name with ''
    column_name = re.sub('[^a-zA-Z]', '', column_name)

    # convert to lower case
    column_name = column_name.lower()

    # primary condition to be classifieeed as a date column

    keywords = ['date', 'year', 'month', 'time']

    for key in keywords:
        if key in column_name:
            try:
                pandas.to_datetime(column)
                return True
            except:
                return False

    # More formats in this can be appended in the future
    # There is a tradeoff between number of formats & execution time
    most_common_formats_list = ['%m/%d/%Y', '%m/%Y/%d', '%d/%m/%Y',
                                '%d/%Y/%m', '%Y/%d/%m', '%Y/%m/%d',
                                '%m-%d-%Y', '%m-%Y-%d', '%d-%m-%Y',
                                '%d-%Y-%m', '%Y-%d-%m', '%Y-%m-%d']

    # Checking if for all the rows is there a format that matches
    for entry in column:
        matched_format_found = False
        for format in most_common_formats_list:
            try:
                datetime.datetime.strptime(entry, format)
                matched_format_found = True
            except:
                pass
        if matched_format_found == False:
            return False

    return True
