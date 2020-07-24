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

import top_down_error
from util.enums import SummaryOperators
from util.enums import Filters

def test_1():
    """
        question :  compare average score of A and B by class.
     """
    table = pandas.read_csv('data/student_score1.csv')
    query_result = top_down_error.top_down_error(table, 'marks',
                                                   ['class', 'student_name', 'subject'],
                                                   'student_name', 'A', 'B',
                                                   SummaryOperators.MEAN,
                                                   dimensions = ['class'])
    print(query_result)

    expected_result = "[{'suggestion': 'Some values are similar here but will vary if we add subject for grouping ', 'oversight_name': 'top-down error', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}, {'row': 3, 'confidence_score': 100}, {'row': 4, 'confidence_score': 100}]}]"
    assert(str(query_result) == expected_result)

def test_2():
    """
        question :  compare average score of A and B by class.
     """
    table = pandas.read_csv('data/student_score2.csv')
    query_result = top_down_error.top_down_error(table, 'marks',
                                                   ['class', 'student_name', 'subject'],
                                                   'student_name', 'A', 'B',
                                                   SummaryOperators.MEAN,
                                                   dimensions = ['class'])
    print(query_result)

    expected_result = "[{'suggestion': 'Some values are similar here but will vary if we add subject for grouping ', 'oversight_name': 'top-down error', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}]}]"
    assert(str(query_result) == expected_result)

print("\ncompare average score of A and B by class.")
test_1()

print("\ncompare average score of A and B by class again.")
test_2()

print("\nTest cases completed")
