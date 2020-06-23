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

""" This module currently contains the basic implementation of calculating
next and the previous time window.
The method used to determine the required time window will be changed later.
To-Do : Calculating the time precision of the time given.
"""

import datetime

def previous(start_date, end_date, date_format):
    """ This functions returns the start date and end date of the previous
    window.
    The method used-
    1. Calculate the time difference between start_date and end_date.
    2. Return the interval of the same length ending at start_date.

    Args:
        start_date - Type-str
            It is the start date of the given time window
        end_date - Type-str
            It is the end date of the given time window
        date_format - Typr-str
            It is the format in which the start_date and end_date are present.
            Format Codes
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

    Returns:
        This function returns the start_date and end_date corresponding to the
        previous window.
    """

    # converting strings to datetime objects
    start_date = datetime.datetime.strptime(start_date, date_format)
    end_date = datetime.datetime.strptime(end_date, date_format)

    # length of window
    delta_time = end_date - start_date

    # calculating previous windows start date
    previous_start_date = start_date - delta_time

    previous_end_date = start_date

    previous_start_date = previous_start_date.strftime(date_format)
    previous_end_date = previous_end_date.strftime(date_format)

    return previous_start_date, previous_end_date
