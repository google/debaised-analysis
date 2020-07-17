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
This module will detect the type(Consistent, all ambiguous, inconsistent column)
a passed column is & also wether day_first is True/False for that column.
"""
import datetime
import pandas
from util import enums

def get_column_type_and_order(column):
    """
    This function classifies the column into the 3 types based on
    the values in it. It also returns the day_first = Bool for the column.

    Args - column - type list
    Returns - dict - {type, day_first}}
                type = attribute of enums.ColumnTypes ex ColumnTypes.CONSISTENT
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
        column_type_and_order['type'] = enums.ColumnTypes.INCONSISTENT
        column_type_and_order['day_first'] = None
    elif count_date_type[True] != 0:
        column_type_and_order['type'] = enums.ColumnTypes.CONSINTENT
        column_type_and_order['day_first'] = True
    elif count_date_type[False] != 0:
        column_type_and_order['type'] = enums.ColumnTypes.CONSINTENT
        column_type_and_order['day_first'] = False
    else:
        column_type_and_order['type'] = enums.ColumnTypes.ALL_AMBIGUOUS
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
    # converting str date to a timestamp format ex- '2019-08-05 17:51:29'
    date_timestamp = str(pandas.to_datetime(date, dayfirst=day_first))

    # converting the timestamp to datetime object
    date_datetime = datetime.datetime.strptime(date_timestamp,
                                               '%Y-%m-%d %H:%M:%S')
    return date_datetime
