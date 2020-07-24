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
    This module has some examples of function calls for queries from
    small part of innings dataset. The query is also mentioned.
"""

import pandas

import time_compare
from util.enums import *

def test_1():
    """
        An example from the IPL dataset
        question :  Compare total_run of team_name ‘MI’ in date_comparision_colum in 
                    between ranges 01/01/2008-31/12/2009 and 01/01/2010-31/12/2011.
    """
    table = pandas.read_csv('data/cricket_data.csv')
    query_result = time_compare.time_compare(table, 'total_run',
                                             ['team_name', 'date_of_match'],
                                             'date_of_match', ('01/01/2008', '31/12/2009'), 
                                              ('01/01/2010', '31/12/2011'), '%d/%m/%Y',
                                             SummaryOperators.SUM,
                                             slices = [('team_name', Filters.EQUAL_TO, 'MI')],
                                             dimensions = ['team_name']
                                             )
    print(query_result[0])

    expected_result = """  team_name            date_of_match  total_run
0        MI  01/01/2008 - 31/12/2009        776
1        MI  01/01/2010 - 31/12/2011        420"""
    expected_suggestions = "[]"

    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

def test_2():
    """
        An example from the IPL dataset
        question :  Compare total number of match played by 'England and Wales' from 
                    '1871-11-30' to '1950-12-30' and '1950-12-31' to '2020-01-01' in 'England'
    """
    table = pandas.read_csv('data/football_matches.csv')

    query_result = time_compare.time_compare(table, 'tournament',
                                             ['home_team', 'away_team', 'date', 'country'],
                                             'date', ('1871-11-30', '1950-12-30'), 
                                              ('1950-12-31', '2020-01-01'), '%Y-%m-%d',
                                             SummaryOperators.COUNT,
                                             slices = [('home_team', Filters.EQUAL_TO, 'England'), 
                                                       ('away_team', Filters.EQUAL_TO, 'Wales'), 
                                                       ('country', Filters.EQUAL_TO, 'England')],
                                             dimensions = ['home_team', 'away_team', 'country'])
    print(query_result)

    expected_result = """  home_team away_team  country                     date  tournament
0   England     Wales  England  1871-11-30 - 1950-12-30          33
1   England     Wales  England  1950-12-31 - 2020-01-01          19"""
    expected_suggestions = "[]"

    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

print("\nCompare total_run of team_name ‘MI’ in date_comparision_colum in between ranges 01/01/2008 - 31/12/2009 and 01/01/2010 - 31/12/2011")
test_1()

print("\nCompare total number of match played by 'England and Wales' from '1871-11-30' to '1950-12-30' and '1950-12-31' to '2020-01-01' in 'England'")
test_2()

print("\nTest cases completed")
