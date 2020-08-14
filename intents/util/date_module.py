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
This module contains functions to detect date from strings using the
parameter day_first.
Day_first denotes that does day in the date occurs before month in the
dates in the date column
Example - '29-02-19', here day_first is true
"""
import datetime
import pandas

def str_to_datetime(date, day_first):
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
