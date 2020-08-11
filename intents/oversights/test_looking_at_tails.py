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
This module contains the tests for looking_at_tails.py

In these tests first the topk is called and the result table is
created with k = -1, then the result table is used to test the
oversights detection.
"""
import sys
sys.path.append(".")

import pandas
import topk
import oversights

def generate_1():
    """
    Generates data required for test_1.
    dataset used - https://www.kaggle.com/odartey/top-chess-players
    Stored in - data/data_for_test_looking_at_tails/fide_historical.csv
    """
    table = pandas.read_csv('data/data_for_test_looking_at_tails/fide_historical.csv')
    result_table = topk.topk_results(table, 'rating',
                                     ['name', 'birth_year', 'games'], False, -1)[0]
    result_table.to_csv('data/data_for_test_looking_at_tails/result_table_for_test_1',
                        index=False)

def generate_2():
    """
    Generates data required for test_2.
    dataset used - randomly generated in util/test_aspects
    Stored in - data/data_for_test_looking_at_tails/fide_historical.csv
    """
    table = pandas.read_csv('data/data_for_test_aspects/test_1.csv')
    result_table = topk.topk_results(table, 'Age', ['Name', 'Gender'], False, -1)[0]
    result_table.to_csv('data/data_for_test_looking_at_tails/result_table_for_test_2',
                        index=False)

def test_1():
    """
    Tests the looking_at_tails based on the result table generated & stored
    in data/data_for_test_looking_at_tails/result_table_for_test_1

    Situation : In this test the oversight occurs for the 'games'
    column (it contains real numbers)
    """
    result_table = pandas.read_csv('data/data_for_test_looking_at_tails/result_table_for_test_1')
    k = 10
    metric = 'rating'

    # The data should be already sorted
    assert(result_table[metric].is_monotonic_decreasing)

    suggestions = oversights.looking_at_tails.looking_at_tails(result_table, k, metric)

    print(suggestions)
    expected_suggestions = """{'suggestion': "Values in top-k rows of columns - 'games' are similar for other rows also", 'oversight': <Oversights.LOOKING_AT_TAILS_TO_FIND_CAUSES: 5>, 'is_column_level_suggestion': True, 'col_list': [{'column': 'games', 'confidence_score': 0.5549613585989281}]}"""

    assert(expected_suggestions == str(suggestions))

def test_2():
    """
    Tests the looking_at_tails based on the result table generated & stored
    in data/data_for_test_looking_at_tails/result_table_for_test_2

    Situation : In this test the oversight occurs for the 'Gender' column (it contains binary variables)
    """
    result_table = pandas.read_csv('data/data_for_test_looking_at_tails/result_table_for_test_2')
    k = 100000
    metric = 'Age'

    # The data should be already sorted
    assert(result_table[metric].is_monotonic_decreasing)

    suggestions = oversights.looking_at_tails.looking_at_tails(result_table, k, metric)

    print(suggestions)
    expected_suggestions = """{'suggestion': "Values in top-k rows of columns - 'Gender' are similar for other rows also", 'oversight': <Oversights.LOOKING_AT_TAILS_TO_FIND_CAUSES: 5>, 'is_column_level_suggestion': True, 'col_list': [{'column': 'Gender', 'confidence_score': 0.05474928826225144}]}"""

    assert(expected_suggestions == str(suggestions))

# print(generate_1.__doc__)
# generate_1()

# print(generate_2.__doc__)
# generate_2()

print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print('Test cases completed')