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
                    'Chennai Super Kings' by season.
     """
    table = pandas.read_csv('data/ipl_innings.csv')
    query_result = slice_compare.slice_compare(table, 'total_runs',
                                               ['batsman_team', 'season'],
                                               ['total_runs'], 'batsman_team', 
                                               'Mumbai Indians', 'Chennai Super Kings',
                                               SummaryOperators.SUM, dimensions = ['season']
                                               )
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
                                               ['Person name', 'year', 'month'],
                                               ['salary'], 'Person name', 'A', 
                                               'B', SummaryOperators.SUM,
                                               slices = [('Person name', Filters.IN, ['A', 'B'])],
                                               dimensions = ['year'])
    print(query_result)

    expected_result = """   year Person name  salary
0  2019           A   10239
1  2019           B    8190"""
    expected_suggestion = "[{'suggestion': 'the relation between slices might changed a lot if you will consider month in grouping.', 'oversight_name': 'simpsons-paradox', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}]}]"

    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestion == str(query_result[1]))

def test_3():
    """
        An example from the IPL dataset
        question :  compare total run scored in 1st innings and second innings by batsman_teams.
     """
    table = pandas.read_csv('data/ipl_innings.csv')
    query_result = slice_compare.slice_compare(table, 'total_runs',
                                               ['batsman_team', 'innings'],
                                               ['total_runs'], 'innings', 
                                               '1st', '2nd', SummaryOperators.SUM,
                                               dimensions = ['batsman_team'],
                                               slices = [('innings', Filters.IN, ['1st', '2nd'])])
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

def test_4():
    """
        question :  compare average hour work per day of A and rest all interns.
     """
    table = pandas.read_csv('data/intern_performance.csv')
    query_result = slice_compare.slice_compare(table, 'avg_hour_of_work',
                                               ['intern_name'], ['avg_hour_of_work', 'lines_of_code'], 
                                              'intern_name', 'A', '*', SummaryOperators.MEAN)
    print(query_result)

    expected_output = """  intern_name  avg_hour_of_work
0           A               8.5
1         ALL               5.5"""
    expected_suggestion = "[{'suggestion': 'A looks different from others on avg_hour_of_work. You might also want to look at lines_of_code since A also looks different on this.', 'oversight_name': 'Benchmark set too different', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}]}]"

    assert(expected_output == query_result[0].to_string())
    assert(expected_suggestion == str(query_result[1]))

def test_5():
    """
        question :  compare average score of A and B by class.
     """
    table = pandas.read_csv('data/student_score1.csv')
    query_result = slice_compare.slice_compare(table, 'marks',
                                               ['class', 'student_name', 'subject'],
                                               ['marks'], 'student_name', 'A', 'B',
                                               SummaryOperators.MEAN,
                                               dimensions = ['class'])
    print(query_result)

    expected_output = """  class student_name  marks
0   7th            A     75
1   7th            B     75
2   8th            A     75
3   8th            B     75"""
    expected_suggestion = "[{'suggestion': 'the relation between slices might changed a lot if you will consider subject in grouping.', 'oversight_name': 'simpsons-paradox', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}]}, {'suggestion': 'Some values are similar here but will vary if we add subject for grouping ', 'oversight_name': 'top-down error', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}, {'row': 3, 'confidence_score': 100}, {'row': 4, 'confidence_score': 100}]}]"

    assert(expected_output == query_result[0].to_string())
    assert(expected_suggestion == str(query_result[1]))

print("\ncompare total runs of 'Mumbai indians' and 'Chennai Super Kings'")
test_1()

print("\ncompare total salary of 'A' and 'B' for year 2019.")
test_2()

print("\ncompare total run scored in 1st innings and second innings by batsman_teams.")
test_3()

print("\ncompare average hour work per day of A and rest all interns.")
test_4()

print("\ncompare average score of A and B by class.")
test_5()

print("\nTest cases completed")
