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
This module contains the tests for topk_vs_others.py

In these tests first the topk is called and the result table is
created without applting the k condition, then the result table is used
to test the oversights detection.
"""
import sys
sys.path.append(".")

import pandas
import topk
from oversights import topk_vs_others

def generate():
    """
    Generates data required for both test_1 & test_2
    dataset used - https://www.contextures.com/xlSampleData01.html

    Top-k query - "Find the top-k Item with minimum UnitCost"

    This function takes stores the result table of the query without
    applying the k condition & stores the result in a csv file.

    the generated result table is used in test_1
    """
    table = pandas.read_csv('data/data_for_test_topk_vs_others/sheet1.csv')
    result_table = topk.topk_results(table, 'UnitCost',
                                     ['Item'], True, -1)
    result_table.to_csv('data/data_for_test_topk_vs_others/result_table.csv',
                        index=False)

def test_1():
    """
    Tests the topk_vs_others based on the result table generated & stored
    in data/data_for_test_topk_vs_others/result_table for the query -
    Top-10 Item based on minimum unit costs.

    Here the top-k vs others suggestion is asserted when the
    ratio = topk_sum / others_sum is positive and is less than
    the threshold
    """
    result_table = pandas.read_csv('data/data_for_test_topk_vs_others/result_table.csv')
    k = 10
    metric = 'UnitCost'

    # The data should be already sorted
    assert(result_table[metric].is_monotonic_increasing)

    # suggestions = oversights.looking_at_tails.looking_at_tails(result_table, k, metric)
    suggestions = topk_vs_others.topk_vs_others(result_table, k, metric)

    print(suggestions)
    expected_suggestions = """{'change_list': {'topKLimit': 43}, 'suggestion': 'The rows NOT in the top-k have a much larger sum over UnitCost than the rows in top-k', 'confidence_score': 0.008621645877239863}"""

    assert(expected_suggestions == str(suggestions))

def test_2():
    """
    The result table without the k-condition is hardcoded for
    the query -
    Top-4 Salespersons with maximum Sales

    Here the top-k vs others suggestion is asserted when the
    ratio = topk_sum / others_sum is positive and is more than
    the threshold, so no suggestion is returned
    """
    # hardcoding the artificial results table
    result_table = pandas.DataFrame()
    result_table['Salesperson'] = pandas.Series(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    result_table['Sales'] = pandas.Series([5, 4, 3, 3, 3, 2, 1])
    k = 4
    metric = 'Sales'

    # The data should be already sorted
    assert(result_table[metric].is_monotonic_decreasing)

    # suggestions = oversights.looking_at_tails.looking_at_tails(result_table, k, metric)
    suggestions = topk_vs_others.topk_vs_others(result_table, k, metric)

    print(suggestions)
    expected_suggestions = """None"""

    assert(expected_suggestions == str(suggestions))

def test_3():
    """
    The result table without the k-condition is hardcoded for
    the query -
    Top-4 Salespersons with maximum Sales

    Here the top-k vs others suggestion is asserted when the
    ratio = topk_sum / others_sum is negative
    """
    # hardcoding the artificial results table
    result_table = pandas.DataFrame()
    result_table['Salesperson'] = pandas.Series(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    result_table['Sales'] = pandas.Series([5, 4, 3, 3, -1, -2, -10])
    k = 4
    metric = 'Sales'

    # The data should be already sorted
    assert(result_table[metric].is_monotonic_decreasing)

    # suggestions = oversights.looking_at_tails.looking_at_tails(result_table, k, metric)
    suggestions = topk_vs_others.topk_vs_others(result_table, k, metric)

    print(suggestions)
    expected_suggestions = """{'change_list': {'topKLimit': 7}, 'suggestion': 'The sum of Sales in top-k rows is negative whereas sum of rows not in top-k is positive', 'confidence_score': -1.1538461538461537}"""

    assert(expected_suggestions == str(suggestions))

# print('Generating top-k results')
# print(generate.__doc__)
# generate()

print('Running tests')

print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_2.__doc__)
test_3()

print('Test cases completed')
