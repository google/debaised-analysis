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

import slice_compare
from util.enums import *

def test_1():
    """
    	An example from the IPL dataset
    	question :  compare total runs of 'Mumbai indians' and
    				'Chennai Super Kings'.
     """
    table = pandas.read_csv('data/ipl_innings.csv')
    query_result = slice_compare.slice_compare(table, 'total_runs',
	                                           ['batsman_team', 'season'],
											   ['batsman_team', 'season'],
											   ['total_runs'],
											   [('batsman_team', Filters.IN, ['Mumbai Indians', 'Chennai Super Kings'])],
											   ['batsman_team', 'Mumbai Indians', 'Chennai Super Kings'],
											   SummaryOperators.SUM)
    print(query_result)

    expected_result = """   season         batsman_team  total_runs
0    2008  Chennai Super Kings         868
1    2008       Mumbai Indians         346"""
    expected_suggestion = """[]"""

    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestion == str(query_result[1]))

def test_2():
    """
    	An example from the IPL dataset
    	question :  compare total salary of 'A' and 'B' for year 2019.
     """
    table = pandas.read_csv('data/salary_list_modified.csv')
    query_result = slice_compare.slice_compare(table, 'salary',
    		['Person name', 'year'], ['Person name', 'year', 'month'],
            ['salary'], [('Person name', Filters.IN, ['A', 'B'])] ,
            ['Person name', 'A', 'B'], SummaryOperators.SUM)
    print(query_result)

    expected_result = """   year Person name  salary
0  2019           A   10239
1  2019           B    8190"""
    expected_suggestion = "['year', 'month', 'Person name'] these group of columns have different results than initial columns so you might also look for the given group of columns"

    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestion == query_result[1][0])

def test_3():
    """
    	An example from the IPL dataset
    	question :  compare total run scored in 1st innings and second innings by batsman_teams.
     """
    table = pandas.read_csv('data/ipl_innings.csv')
    query_result = slice_compare.slice_compare(table, 'total_runs',
    		['batsman_team', 'innings'], ['batsman_team', 'innings'], ['total_runs'],
             [('innings', Filters.IN, ['1st', '2nd'])], ['innings', '1st', '2nd'],
                            SummaryOperators.SUM)
    print(query_result)

    expected_output = """                   batsman_team innings  total_runs
0           Chennai Super Kings     1st         544
1           Chennai Super Kings     2nd         324
2               Deccan Chargers     1st          40
3               Deccan Chargers     2nd         102
4              Delhi Daredevils     1st         248
5              Delhi Daredevils     2nd         342
6                 Gujarat Lions     1st         100
7                 Gujarat Lions     2nd           4
8               Kings XI Punjab     1st         448
9               Kings XI Punjab     2nd         522
10        Kolkata Knight Riders     1st         338
11        Kolkata Knight Riders     2nd         708
12               Mumbai Indians     1st         330
13               Mumbai Indians     2nd          16
14                Pune Warriors     1st          12
15                Pune Warriors     2nd         158
16             Rajasthan Royals     1st         368
17             Rajasthan Royals     2nd         608
18  Royal Challengers Bangalore     1st         866
19  Royal Challengers Bangalore     2nd         136
20          Sunrisers Hyderabad     1st          63
21          Sunrisers Hyderabad     2nd         331"""
    expected_suggestion = """[]"""

    assert(expected_output == query_result[0].to_string())
    assert(expected_suggestion == str(query_result[1]))

print("\ncompare total runs of 'Mumbai indians' and 'Chennai Super Kings'")
test_1()

print("\ncompare total salary of 'A' and 'B' for year 2019.")
test_2()

print("\ncompare total run scored in 1st innings and second innings by batsman_teams.")
test_3()

print("\nTest cases completed")
