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
And then classifies each date column into 3 types-
1. Consistent  - (There is atleast 1 unabiguous date in the column & all
                  unambiguous dates follow same date order)
2. Inconsistent - (Set of unambiguous dates don't follow the same date order)
3. All Ambiguous - (No date is unambiguous)

And if the column type is 'Consistent' then it also
returns date_first = True / False.

date_first = Bool is an extra argument required of parsing ambiguous dates.
"""

import re
import datetime
import pandas

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
    # initialized the possible date columns to all the columns.
    date_columns = []

    # for each column in the table if it has 'date' as a substring or
    # it follows any 6 of the date formats we consider it as a date column.
    for column in table.columns:
        # passing only the column instead of entire table is efficient
        column_as_list = table[column].tolist()
        if _possible_date_column(column_as_list, column):
            date_columns.append(column)

    # this will return a dict { 'date_column_name' : {type_str, day_first}}
    # type_str = 'Consistent' / 'all ambiguous' / 'inconsistent column'
    # in case of 'Constient' column day_first = True / False
    # in other cases day_first = None

    column_type_and_order = {}

    for column in date_columns:
        column_type_and_order[column] = _get_column_type_and_order(table[column].tolist())

    return column_type_and_order

def _get_column_type_and_order(column):
    """
    This function classifies the column into the 3 types based on
    the values in it. It also returns the day_first = Bool for the column.

    Args - column - type list
    Returns - dict - {type_str, day_first}}
                type_str = 'Consistent' / 'all ambiguous' / 'Inconsistent'
                in case of 'Constient' column day_first = True / False
    """
    # Convert integers in the list to strings
    column = [str(entry) for entry in column]

    # True / False for unambiguous dates & None for ambiguous dates
    count_date_type = {True : 0, False : 0, None : 0}

    for date in column:
        # if month & day can be interchanged for a date we consider it ambiguous
        if _to_datetime(date, True) != _to_datetime(date, False) or \
           _to_datetime(date, True).month == _to_datetime(date, True).day:
            count_date_type[None] += 1
        elif _is_day_first(date):
            count_date_type[True] += 1
        else:
            count_date_type[False] += 1

    column_type_and_order = {}

    if count_date_type[True] != 0 and count_date_type[False] != 0:
        # Inconsistent type column
        column_type_and_order['type_str'] = 'Inconsistent'
        column_type_and_order['day_first'] = None
    elif count_date_type[True] != 0:
        column_type_and_order['type_str'] = 'Constient'
        column_type_and_order['day_first'] = True
    elif count_date_type[False] != 0:
        column_type_and_order['type_str'] = 'Constient'
        column_type_and_order['day_first'] = False
    else:
        column_type_and_order['type_str'] = 'All ambiguous'
        column_type_and_order['day_first'] = None

    return column_type_and_order


def _is_day_first(date):
    """
    This function looks into the date(string) and decides if
    day occurs first in it. Date passed should be unambiguous.
    Args :
        date - Type string
    Returns :
        Bool - True if day occurs before month.
    """
    date_datetime = _to_datetime(date, None)

    # Removing time from the date
    # Here it is assumed that time is present in the from '%H:%M:%S'
    # Other possible time formats can be added to the list possible_times

    date_without_time = date

    possible_times = [_to_str(date_datetime.hour) + ':' +
                      _to_str(date_datetime.minute) + ':' +
                      _to_str(date_datetime.second)]

    if date.find(possible_times[0]) != -1:
        date_without_time = date.replace(possible_times[0], '')

    date = date_without_time

    # Removing Year from the date
    # Only last 2 digits of year may be present
    # Ex. sometines 1998 is represented as 98

    date_without_year = date

    # List of possible years mentioned in date
    possible_years = [str(date_datetime.year), str(date_datetime.year % 100)]

    if date.find(possible_years[0]) != -1:
        date_without_year = date.replace(possible_years[0], '')
    else:
        date_without_year = date.replace(possible_years[1], '')

    date = date_without_year

    # Now as both time and year are removed from date string we are only left
    # with day & month

    return date.find(str(date_datetime.day)) < date.find(str(date_datetime.month))

def _to_str(num):
    """
    This function converts the number passed to a string,
    it just adds a '0' if number passed is of single digit.
    Args :
        num - int
    Returns :
        string
    """
    if num < 10:
        return '0' + str(num)
    else:
        return str(num)

def _to_datetime(date, day_first):
    """
    As pandas to_datetime returns a timestramp - this function converts it to
    a datetime object using the strptime method.
    Args :
        date - string representing date
        day_first - Bool/None
            Argument required to parse ambiguous dates.
    Returns :
        date as a datetime object
    """
    date_timestamp = str(pandas.to_datetime(date, dayfirst=day_first))
    date_datetime = datetime.datetime.strptime(date_timestamp,
                                               '%Y-%m-%d %H:%M:%S')
    return date_datetime
