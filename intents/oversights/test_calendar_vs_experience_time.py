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
This module contains tests for oversight calendar vs experience
in time series.
"""

import sys  
sys.path.append(".")

import pandas

import calendar_vs_experience_time
from util.enums import SummaryOperators
from util.enums import Filters

def test_1():
    """
        query :  compare average sales of A and B in date range 2000 to 2010
        here the oversight is detected as the 2 companies differ in experience
        time.
    """
    table = pandas.DataFrame()
    table['Company'] = pandas.Series(['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'])
    table['year'] = pandas.Series(['2001', '2006', '2002', '2007', '2003', '2008', '2004', '2009'])
    table['sales'] = pandas.Series([1, 34, 23, 42, 23, 1324, 34, 134])
    print(table)
    suggestion = calendar_vs_experience_time.calendar_vs_experience_time(table, 'sales',
                                                   ['Company', 'year', 'sales'],
                                                   'Company', 'A', 'B',
                                                   SummaryOperators.MEAN,
                                                   date_column_name='year',
                                                   date_range=['2000-01-01', '2010-01-01'],
                                                   date_format='%Y')
    print(suggestion)

    expected_suggestion = "{'oversight': <Oversights.CALENDAR_VS_EXPERIENCE_IN_TIME_SERIES: 12>, 'confidence_score': 1.0, 'suggestion': 'The entries in the date range mentioned are not consistent for both the slices'}"
    assert(str(suggestion) == expected_suggestion)

def test_2():
    """
        query :  compare average sales of A and B in date range 2000 to 2010
        here the oversight is not detected as the 2 companies don't differ in 
        experience time
    """
    table = pandas.DataFrame()
    table['Company'] = pandas.Series(['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'])
    table['year'] = pandas.Series(['2001', '2001', '2002', '2002', '2006', '2006', '2007', '2007'])
    table['sales'] = pandas.Series([1, 34, 23, 42, 23, 1324, 34, 134])
    print(table)
    suggestion = calendar_vs_experience_time.calendar_vs_experience_time(table, 'sales',
                                                   ['Company', 'year', 'sales'],
                                                   'Company', 'A', 'B',
                                                   SummaryOperators.MEAN,
                                                   date_column_name='year',
                                                   date_range=['2000-01-01', '2010-01-01'],
                                                   date_format='%Y')
    print(suggestion)

    expected_suggestion = 'None'
    assert(str(suggestion) == expected_suggestion)

print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print("Test cases completed")
