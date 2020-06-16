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

"""This module has some examples of function calls for queries
from IPL matches.csv
The query is mentiond in __doc__ of the function.
"""

import pandas

import show
from util.enums import *


def test_1():
    """An example from the IPL dataset 
    question : show all cities in season 2017 in the
    			date range 2008-05-08 to 2017-04-12
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
    							dimensions=['city'],
    	                        slices={'season' : 2017},
    	                        date_range=('2008-05-08', '2017-04-12'),
    	                        date_column_name='date',
    	                        date_format='%Y-%m-%d')


    print(query_result);
    expected_result = """        city
0  Hyderabad
1       Pune
2     Rajkot
3     Indore
4  Bangalore
5  Hyderabad
6     Mumbai
7     Indore
8       Pune
9     Mumbai"""
    assert(expected_result == query_result.to_string())


def test_2():
    """An example from the IPL dataset
    question :show player_of_match along with their average of win_by_runs
              in season 2017 in date range 2008-05-08 to 2017-04-12
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
    							dimensions = ['player_of_match'],
    							metric = 'win_by_runs' ,
    	                        slices={'season' : 2017},
    	                        date_range=('2017-05-09', '2017-05-12'),
    	                        date_column_name='date', date_format='%Y-%m-%d',
    	                        summary_operator=SummaryOperators.MEAN)
    print(query_result)
    expected_result = """  player_of_match  win_by_runs
0         KK Nair            7
1       MM Sharma           14
2         SS Iyer            0
3         WP Saha            7"""
    assert(expected_result == query_result.to_string())


print(test_1.__doc__)
test_1()    
print(test_2.__doc__)
test_2()

print("Test cases completed")