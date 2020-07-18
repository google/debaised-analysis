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

import sys  
sys.path.append(".")

import pandas

import simpsons_paradox
from util.enums import SummaryOperators
from util.enums import Filters

def test_1():
    """
        question :  compare total salary of 'A' and 'B' by year.
     """
    table = pandas.read_csv('data/salary_list_modified.csv')
    query_result = simpsons_paradox.simpsons_paradox(table, 'salary',
                                                   ['Person name', 'month', 'year'],
                                                   'Person name', 'A', 'B',
                                                   SummaryOperators.SUM,
                                                   dimensions = ['year'])
    print(query_result)

    expected_result = "[{'suggestion': 'the relation between slices might changed a lot if you will consider month in grouping.', 'oversight_name': 'simpsons-paradox', 'is_row_level_suggestion': True, 'row_list': [0, 1]}]"
    assert(str(query_result) == expected_result)

def test_2():
    """
        question :  compare avg run for 'MI' and 'CSK' by city.
     """
    table = pandas.read_csv('data/ipl_example.csv')
    query_result = simpsons_paradox.simpsons_paradox(table, 'run_scored',
                                                   ['team_name', 'city'],
                                                   'team_name', 'MI', 'CSK',
                                                   SummaryOperators.MEAN)
    print(query_result)

    expected_result = "[{'suggestion': 'the relation between slices might changed a lot if you will consider city in grouping.', 'oversight_name': 'simpsons-paradox', 'is_row_level_suggestion': True, 'row_list': [0, 1]}]"
    assert(str(query_result) == expected_result)

def test_3():
    """
        question :  compare average score of A and B by class.
     """
    table = pandas.read_csv('data/student_score.csv')
    query_result = simpsons_paradox.simpsons_paradox(table, 'marks',
                                                   ['class', 'student_name', 'subject'],
                                                   'student_name', 'A', 'B',
                                                   SummaryOperators.MEAN,
                                                   dimensions = ['class'])
    print(query_result)

    expected_result = "[{'suggestion': 'the relation between slices might changed a lot if you will consider subject in grouping.', 'oversight_name': 'simpsons-paradox', 'is_row_level_suggestion': True, 'row_list': [0, 1, 2, 3]}]"
    assert(str(query_result) == expected_result)

def test_4():
    """
        question :  compare average score of A and B by class.
     """
    table = pandas.read_csv('data/student_score_again.csv')
    query_result = simpsons_paradox.simpsons_paradox(table, 'marks',
                                                   ['class', 'student_name', 'subject'],
                                                   'student_name', 'A', 'B',
                                                   SummaryOperators.MEAN,
                                                   dimensions = ['class'])
    print(query_result)

    expected_result = "[{'suggestion': 'the relation between slices might changed a lot if you will consider subject in grouping.', 'oversight_name': 'simpsons-paradox', 'is_row_level_suggestion': True, 'row_list': [0, 1]}]"
    assert(str(query_result) == expected_result)

def test_5():
    """
        question :  compare average revenue of A and B by country.
     """
    table = pandas.read_csv('data/new_revenue_list.csv')
    query_result = simpsons_paradox.simpsons_paradox(table, 'revenue',
                                                   ['country_name', 'company_name', 'month'],
                                                   'company_name', 'A', 'B',
                                                   SummaryOperators.MEAN,
                                                   dimensions = ['country_name'])
    print(query_result)

    expected_result = "[{'suggestion': 'the relation between slices might changed a lot if you will consider month in grouping.', 'oversight_name': 'simpsons-paradox', 'is_row_level_suggestion': True, 'row_list': [2]}]"
    assert(str(query_result) == expected_result)

print("\ncompare total salary of 'A' and 'B' for year 2019.")
test_1()

print("\ncompare avg run for 'MI' and 'CSK' by city.")
test_2()

print("\ncompare average score of A and B by class.")
test_3()

print("\ncompare average score of A and B by class again.")
test_4()

print("\ncompare average revenue of A and B by country.")
test_5()

print("\nTest cases completed")
