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
This module adds the functionality of prefilling the minimum date &
maximum date in the card for filling start date & end date for slicing 
based on date range aspect
"""
import pandas
import datetime
from util import enums

def update_min_max_date(column_type_and_order, table):
    """
    This function takes the dict of date columns (column_type_and_order) and the
    entire table as pandas dataframe and adds keys representing minimum dates and
    maximum dates of each of the Consistent & All Ambiguous date columns.
    
    In the dict for each of the Consistent & All_ambiguous date columns 2 keys,
    min_date & max_date are added.
    Example - 

    # Consistent column with day_first = True
    'Order_date' : {
         # rest of the keys remain the same
         # new key added -
         min_date : {
            'day_first_false': '2001-02-02'
         }
         max_date : {
            'day_first_false': '2024-07-03'
         }
    }

    # All Ambiguous column
    'Shipping_date' : {
         # rest of the keys remain the same
         # new key added -
         min_date : {
            'day_first_false': '2019-08-01' # min date if user selects day_first = False
            'day_first_true': '2019-04-01'
         }
         max_date : {
            'day_first_false': '2020-11-03'
            'day_first_true': '2020-03-11'
         }
    }

    Args :
        column_type_and_order : Type - dict, consists of date column names as keys and their
            corresponding types date order as values.
        table : Type-Pandas Dataframe
    Returns :
        The updated column_type_and_order with the keys min_date & max_date.
    """
    for column in column_type_and_order.keys():
        
        if column_type_and_order[column]['type'] == enums.ColumnTypes.CONSISTENT:

            day_first = column_type_and_order[column]['day_first']

            day_first_key = 'day_first_'

            if day_first :
                day_first_key += 'true'
            else:
                day_first_key += 'false'

            min_date = {}
            min_date[day_first_key] = calculate_min_date(table[column], day_first)
            column_type_and_order[column]['min_date'] = min_date


            max_date = {}
            max_date[day_first_key] = calculate_max_date(table[column], day_first)
            column_type_and_order[column]['max_date'] = max_date

        if column_type_and_order[column]['type'] == enums.ColumnTypes.ALL_AMBIGUOUS:

            min_date = {}
            min_date['day_first_true'] = calculate_min_date(table[column], True)
            min_date['day_first_false'] = calculate_min_date(table[column], False)
            column_type_and_order[column]['min_date'] = min_date

            max_date = {}
            max_date['day_first_true'] = calculate_max_date(table[column], True)
            max_date['day_first_false'] = calculate_max_date(table[column], False)
            column_type_and_order[column]['max_date'] = max_date

    return column_type_and_order

def calculate_min_date(date_list, day_first):
    """
    This function returns the minimum date occuring in the date_list.
    Also, this returns the string in a fixed format 'YYYY-MM-DD'
    Args :
        date_list: pandas series of strings representing dates.
        day_first: Type-Bool, of the dates in the pandas series.
    Returns :
        String representing minimum of all dates occuring in the date list passed
        in a fixed format 'YYYY-MM-DD'.
    """
    date_list = pandas_series_to_datetime(date_list, day_first)
    min_date = min(date_list)
    min_date = min_date.strftime('%Y-%m-%d')
    return min_date


def calculate_max_date(date_list, day_first):
    """
    This function returns the maximum date occuring in the date_list.
    Also, this returns the string in a fixed format 'YYYY-MM-DD'
    Args :
        date_list: pandas series of strings representing dates.
        day_first: Type-Bool, of the dates in the pandas series.
    Returns :
        String representing maximum of all dates occuring in the date list passed
        in a fixed format 'YYYY-MM-DD'.
    """
    date_list = pandas_series_to_datetime(date_list, day_first)
    max_date = max(date_list)
    max_date = max_date.strftime('%Y-%m-%d')
    return max_date

def pandas_series_to_datetime(date_list, day_first):
    """This function converts the pandas series to a list of
    datettime objects.
    Args :
        date_list: pandas series of strings representing dates.
        day_first: Type-Bool, of the dates in the pandas series.
    Returns :
        List of datetime objects.
    """
    date_list = list(date_list)
    date_list = [_to_datetime(date, day_first) for date in date_list]
    return date_list

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
